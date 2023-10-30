import numpy as np
from einops import rearrange
from torch.utils.data import Dataset

__all__ = [
    "Points2Dataset",
]

# pylint: disable=import-outside-toplevel, import-error, unused-argument, too-many-instance-attributes, too-many-arguments


def swissroll_generate_sample(N, noise=0.25):
    import sklearn.datasets as skd

    data = skd.make_swiss_roll(n_samples=N, noise=noise)[0]
    data = data.astype("float32")[:, [0, 2]]
    return data


def moon_generate_sample(N, noise=0.25):
    import sklearn.datasets as skd

    data = skd.make_moons(n_samples=N, noise=noise)[0]
    data = data.astype("float32")
    return data


def checkerboard_generate_sample(N, noise=0.25):
    x1 = np.random.rand(N) * 4 - 2
    x2_ = np.random.rand(N) - np.random.randint(0, 2, N) * 2
    x2 = x2_ + (np.floor(x1) % 2)
    return np.concatenate([x1[:, None], x2[:, None]], 1) * 2


def line_generate_sample(N, noise=0.25):
    assert noise <= 1.0
    cov = np.array([[1.0, 1 - noise], [1 - noise, 1.0]])
    mean = np.array([0.0, 0.0])
    return np.random.multivariate_normal(mean, cov, N)


def circle_generate_sample(N, noise=0.25):
    angle = np.random.uniform(high=2 * np.pi, size=N)
    random_noise = np.random.normal(scale=np.sqrt(0.2), size=(N, 2))
    pos = np.concatenate([np.cos(angle), np.sin(angle)])
    pos = rearrange(pos, "(b c) -> c b", b=2)
    return pos + noise * random_noise


def olympic_generate_sample(N, noise=0.25):
    w = 3.5
    h = 1.5
    centers = np.array([[-w, h], [0.0, h], [w, h], [-w * 0.6, -h], [w * 0.6, -h]])
    pos = [
        circle_generate_sample(N // 5, noise) + centers[i : i + 1] / 2 for i in range(5)
    ]
    return np.concatenate(pos)


def four_generate_sample(N, noise=0.25):
    w = 3.5
    h = 1.5
    centers = np.array([[0.0, h], [w, h], [-w * 0.6, -h], [w * 0.6, -h]])
    pos = [
        circle_generate_sample(N // 4, noise) + centers[i : i + 1] / 2 for i in range(4)
    ]
    return np.concatenate(pos)


def spirals_sample(N, noise=0.25):
    n = np.sqrt(np.random.rand(N // 2, 1)) * 540 * (2 * np.pi) / 360
    d1x = -np.cos(n) * n + np.random.rand(N // 2, 1) * 0.5
    d1y = np.sin(n) * n + np.random.rand(N // 2, 1) * 0.5
    x = np.vstack((np.hstack((d1x, d1y)), np.hstack((-d1x, -d1y)))) / 3
    x += np.random.randn(*x.shape) * 0.1
    return x


def gaussian_sample(N, noise=0.25):
    scale = 4.0
    centers = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
        (1.0 / np.sqrt(2), 1.0 / np.sqrt(2)),
        (1.0 / np.sqrt(2), -1.0 / np.sqrt(2)),
        (-1.0 / np.sqrt(2), 1.0 / np.sqrt(2)),
        (-1.0 / np.sqrt(2), -1.0 / np.sqrt(2)),
    ]
    centers = [(scale * x, scale * y) for x, y in centers]

    dataset = []
    for _ in range(N):
        point = np.random.randn(2) * 0.5
        idx = np.random.randint(8)
        center = centers[idx]
        point[0] += center[0]
        point[1] += center[1]
        dataset.append(point)
    dataset = np.array(dataset, dtype="float32")
    dataset /= 1.414
    return dataset


SKD_FUNC = {
    "swissroll": swissroll_generate_sample,
    "checkerboard": checkerboard_generate_sample,
    "line": line_generate_sample,
    "circle": circle_generate_sample,
    "olympic": olympic_generate_sample,
    "moon": moon_generate_sample,
    "four": four_generate_sample,
    "8gaussian": gaussian_sample,
    "2spirals": spirals_sample,
}


class Points2Dataset(Dataset):
    def __init__(
        self, data_name, num_sample, noise, dim_range=1.0, iscenter=True, shuffle=True
    ):
        self.name = data_name
        self.num_sample = num_sample
        self.noise = noise
        self.iscenter = iscenter
        self.dim_linspace = np.linspace(-dim_range, dim_range, 200)
        self.dim_range = dim_range
        self.shuffle = shuffle

        self.data = self.generate_sample()

    def generate_sample(self):
        data = SKD_FUNC[self.name](self.num_sample, self.noise)
        _max = np.max(np.abs(data))
        data = (self.dim_range * 0.85 / _max) * data
        if self.shuffle:
            np.random.shuffle(data)
        return data

    def __len__(self):
        return self.num_sample - 1

    def __getitem__(self, idx):
        return self.data[idx]
