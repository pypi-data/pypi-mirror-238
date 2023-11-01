# =============================================================================
# MIT License

# Copyright (c) 2023 Reinforcement Learning Evolution Foundation

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# =============================================================================


from typing import Dict, Tuple

import gymnasium as gym
import numpy as np
import torch as th
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader, TensorDataset

from rllte.common.prototype import BaseIntrinsicRewardModule


class Encoder(nn.Module):
    """Encoder for encoding observations.

    Args:
        obs_shape (Tuple): The data shape of observations.
        action_dim (int): The dimension of actions.
        latent_dim (int): The dimension of encoding vectors.

    Returns:
        Encoder instance.
    """

    def __init__(self, obs_shape: Tuple, action_dim: int, latent_dim: int) -> None:
        super().__init__()

        # visual
        if len(obs_shape) == 3:
            self.trunk = nn.Sequential(
                nn.Conv2d(obs_shape[0], 32, kernel_size=3, stride=2, padding=1),
                nn.ELU(),
                nn.Conv2d(32, 32, kernel_size=3, stride=2, padding=1),
                nn.ELU(),
                nn.Conv2d(32, 32, kernel_size=3, stride=2, padding=1),
                nn.ELU(),
                nn.Conv2d(32, 32, kernel_size=3, stride=2, padding=1),
                nn.ELU(),
                nn.Flatten(),
            )
            with th.no_grad():
                sample = th.ones(size=tuple(obs_shape))
                n_flatten = self.trunk(sample.unsqueeze(0)).shape[1]

            self.linear = nn.Linear(n_flatten, latent_dim)
        else:
            self.trunk = nn.Sequential(nn.Linear(obs_shape[0], 256), nn.ReLU())
            self.linear = nn.Linear(256, latent_dim)

    def forward(self, obs: th.Tensor) -> th.Tensor:
        """Encode the input tensors.

        Args:
            obs (th.Tensor): Observations.

        Returns:
            Encoding tensors.
        """
        return self.linear(self.trunk(obs))


class InverseDynamicsModel(nn.Module):
    """Inverse model for reconstructing transition process.

    Args:
        latent_dim (int): The dimension of encoding vectors of the observations.
        action_dim (int): The dimension of predicted actions.

    Returns:
        Model instance.
    """

    def __init__(self, latent_dim, action_dim) -> None:
        super().__init__()

        self.trunk = nn.Sequential(nn.Linear(2 * latent_dim, 256), nn.ReLU(), nn.Linear(256, action_dim))

    def forward(self, obs: th.Tensor, next_obs: th.Tensor) -> th.Tensor:
        """Forward function for outputing predicted actions.

        Args:
            obs (th.Tensor): Current observations.
            next_obs (th.Tensor): Next observations.

        Returns:
            Predicted actions.
        """
        return self.trunk(th.cat([obs, next_obs], dim=1))


class ForwardDynamicsModel(nn.Module):
    """Forward model for reconstructing transition process.

    Args:
        latent_dim (int): The dimension of encoding vectors of the observations.
        action_dim (int): The dimension of predicted actions.

    Returns:
        Model instance.
    """

    def __init__(self, latent_dim, action_dim) -> None:
        super().__init__()

        self.trunk = nn.Sequential(
            nn.Linear(latent_dim + action_dim, 256),
            nn.ReLU(),
            nn.Linear(256, latent_dim),
        )

    def forward(self, obs: th.Tensor, pred_actions: th.Tensor) -> th.Tensor:
        """Forward function for outputing predicted next-obs.

        Args:
            obs (th.Tensor): Current observations.
            pred_actions (th.Tensor): Predicted observations.

        Returns:
            Predicted next-obs.
        """
        return self.trunk(th.cat([obs, pred_actions], dim=1))


class ICM(BaseIntrinsicRewardModule):
    """Curiosity-Driven Exploration by Self-Supervised Prediction.
        See paper: http://proceedings.mlr.press/v70/pathak17a/pathak17a.pdf

    Args:
        observation_space (Space): The observation space of environment.
        action_space (Space): The action space of environment.
        device (str): Device (cpu, cuda, ...) on which the code should be run.
        beta (float): The initial weighting coefficient of the intrinsic rewards.
        kappa (float): The decay rate.
        latent_dim (int): The dimension of encoding vectors.
        lr (float): The learning rate.
        batch_size (int): The batch size for update.

    Returns:
        Instance of ICM.
    """

    def __init__(
        self,
        observation_space: gym.Space,
        action_space: gym.Space,
        device: str = "cpu",
        beta: float = 0.05,
        kappa: float = 0.000025,
        latent_dim: int = 128,
        lr: float = 0.001,
        batch_size: int = 64,
    ) -> None:
        super().__init__(observation_space, action_space, device, beta, kappa)
        self.encoder = Encoder(
            obs_shape=self._obs_shape,
            action_dim=self._action_dim,
            latent_dim=latent_dim,
        ).to(self._device)

        self.im = InverseDynamicsModel(latent_dim=latent_dim, action_dim=self._action_dim).to(self._device)
        if self._action_type == "Discrete":
            self.im_loss = nn.CrossEntropyLoss()
        else:
            self.im_loss = nn.MSELoss()  # type: ignore[assignment]

        self.fm = ForwardDynamicsModel(latent_dim=latent_dim, action_dim=self._action_dim).to(self._device)

        self.encoder_opt = th.optim.Adam(self.encoder.parameters(), lr=lr)
        self.im_opt = th.optim.Adam(self.im.parameters(), lr=lr)
        self.fm_opt = th.optim.Adam(self.fm.parameters(), lr=lr)
        self.batch_size = batch_size

    def compute_irs(self, samples: Dict, step: int = 0) -> th.Tensor:
        """Compute the intrinsic rewards for current samples.

        Args:
            samples (Dict): The collected samples. A python dict like
                {obs (n_steps, n_envs, *obs_shape) <class 'th.Tensor'>,
                actions (n_steps, n_envs, *action_shape) <class 'th.Tensor'>,
                rewards (n_steps, n_envs) <class 'th.Tensor'>,
                next_obs (n_steps, n_envs, *obs_shape) <class 'th.Tensor'>}.
            step (int): The global training step.

        Returns:
            The intrinsic rewards.
        """
        # compute the weighting coefficient of timestep t
        beta_t = self._beta * np.power(1.0 - self._kappa, step)
        num_steps = samples["obs"].size()[0]
        num_envs = samples["obs"].size()[1]
        obs_tensor = samples["obs"].to(self._device)
        actions_tensor = samples["actions"].to(self._device)
        if self._action_type == "Discrete":
            actions_tensor = F.one_hot(actions_tensor.long(), self._action_dim).float()
        next_obs_tensor = samples["next_obs"].to(self._device)

        intrinsic_rewards = th.zeros(size=(num_steps, num_envs))

        with th.no_grad():
            for i in range(num_envs):
                encoded_obs = self.encoder(obs_tensor[:, i])
                encoded_next_obs = self.encoder(next_obs_tensor[:, i])
                pred_next_obs = self.fm(encoded_obs, actions_tensor[:, i])
                dist = th.linalg.vector_norm(encoded_next_obs - pred_next_obs, ord=2, dim=1)
                intrinsic_rewards[:, i] = dist.cpu()

        self.update(samples)

        return intrinsic_rewards * beta_t

    def add(self, samples: Dict) -> None:
        """Add new samples to the intrinsic reward module."""

    def update(self, samples: Dict) -> None:
        """Update the intrinsic reward module if necessary.

        Args:
            samples: The collected samples. A python dict like
                {obs (n_steps, n_envs, *obs_shape) <class 'th.Tensor'>,
                actions (n_steps, n_envs, *action_shape) <class 'th.Tensor'>,
                rewards (n_steps, n_envs) <class 'th.Tensor'>,
                next_obs (n_steps, n_envs, *obs_shape) <class 'th.Tensor'>}.

        Returns:
            None
        """
        num_steps = samples["obs"].size()[0]
        num_envs = samples["obs"].size()[1]
        obs_tensor = samples["obs"].view((num_envs * num_steps, *self._obs_shape)).to(self._device)
        next_obs_tensor = samples["next_obs"].view((num_envs * num_steps, *self._obs_shape)).to(self._device)

        if self._action_type == "Discrete":
            actions_tensor = samples["actions"].view(num_envs * num_steps).to(self._device)
            actions_tensor = F.one_hot(actions_tensor.long(), self._action_dim).float()
        else:
            actions_tensor = samples["actions"].view((num_envs * num_steps, self._action_dim)).to(self._device)

        dataset = TensorDataset(obs_tensor, actions_tensor, next_obs_tensor)
        loader = DataLoader(dataset=dataset, batch_size=self.batch_size)

        for _idx, batch in enumerate(loader):
            obs, actions, next_obs = batch

            self.encoder_opt.zero_grad()
            self.im_opt.zero_grad()
            self.fm_opt.zero_grad()

            encoded_obs = self.encoder(obs)
            encoded_next_obs = self.encoder(next_obs)

            pred_actions = self.im(encoded_obs, encoded_next_obs)
            im_loss = self.im_loss(pred_actions, actions)
            pred_next_obs = self.fm(encoded_obs, actions)
            fm_loss = F.mse_loss(pred_next_obs, encoded_next_obs)
            (im_loss + fm_loss).backward()

            self.encoder_opt.step()
            self.im_opt.step()
            self.fm_opt.step()
