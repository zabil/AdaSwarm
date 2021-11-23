from typing import Tuple
import unittest
from torch import device as torch_device, randint, Tensor, tensor 
from adaswarm.particle import ParticleSwarm, RotatedEMParticle
from unittest.mock import patch


NUMBER_OF_CLASSES = 10
DIMENSION = 125

targets = randint(
    low=0,
    high=NUMBER_OF_CLASSES,
    size=(DIMENSION, NUMBER_OF_CLASSES),
    device=torch_device("cpu"),
    requires_grad=False,
)


class TestParticleSwarm(unittest.TestCase):
    def test_swarm_size(self):
        swarm = ParticleSwarm(
            swarm_size=2,
            targets=targets,
            dimension=DIMENSION,
            number_of_classes=NUMBER_OF_CLASSES,
        )
        self.assertEqual(len(swarm), 2)

    def test_initialise_swarm(self):
        swarm = ParticleSwarm(
            swarm_size=2,
            targets=targets,
            dimension=DIMENSION,
            number_of_classes=NUMBER_OF_CLASSES,
        )
        self.assertIsInstance(swarm[0], RotatedEMParticle)

    def test_update_velocities(self):
        swarm = ParticleSwarm(
            swarm_size=2,
            targets=targets,
            dimension=DIMENSION,
            number_of_classes=NUMBER_OF_CLASSES,
        )

        gbest_position = Tensor(
            size=(DIMENSION, NUMBER_OF_CLASSES), device=torch_device("cpu")
        )

        gbest_position = gbest_position.fill_(0.3)

        with patch("torch.rand", return_value=tensor([0.5])):
            swarm.update_velocities(gbest_position)

        self.assertAlmostEqual(swarm[0].c_1_r_1, 0.45)
        self.assertAlmostEqual(swarm[1].c_1_r_1, 0.45)
        self.assertAlmostEqual(swarm[0].c_2_r_2, 0.4)
        self.assertAlmostEqual(swarm[1].c_2_r_2, 0.4)

    def test_calculate_swarm_scaled_coeffiecient_average(self):
        swarm = ParticleSwarm(
            swarm_size=2,
            targets=targets,
            dimension=DIMENSION,
            number_of_classes=NUMBER_OF_CLASSES,
        )

        gbest_position = Tensor(
            size=(DIMENSION, NUMBER_OF_CLASSES), device=torch_device("cpu")
        )

        gbest_position = gbest_position.fill_(0.3)

        with patch("torch.rand", return_value=tensor([0.5])):
            swarm.update_velocities(gbest_position=gbest_position)

        self.assertAlmostEqual(
            swarm.average_of_scaled_acceleration_coefficients(), 0.85
        )

        # self.assertAlmostEqual(swarm.sum_of_c_2_r_2(), 0.8)


if __name__ == "__main__":
    unittest.main()
