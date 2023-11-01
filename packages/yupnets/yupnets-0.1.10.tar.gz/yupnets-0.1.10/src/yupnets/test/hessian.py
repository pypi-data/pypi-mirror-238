from typing import Optional, Sequence

from copy import deepcopy
import matplotlib.pyplot as plt
from pyhessian import hessian
import torch
from torch.utils.data import DataLoader
import tqdm

__all__ = [
    "HessianTest3D",
]


class HessianTest3D:
    def __init__(
            self,
            model,
            criterion=torch.nn.CrossEntropyLoss(),
            lams: Sequence[float] = torch.linspace(-1, 1, 21),
            batch_size: Optional[int] = 64,
            use_cuda: bool = False,
            verbose: bool = False,
    ) -> None:
        self.machine = "cuda" if use_cuda else "cpu"
        self.model_orig = getattr(model.eval(), self.machine)()
        self.model_pert1 = getattr(deepcopy(model).eval(), self.machine)()
        self.model_pert2 = getattr(deepcopy(model).eval(), self.machine)()

        self.criterion = criterion
        self.lams = lams
        self.batch_size = batch_size
        self.use_cuda = use_cuda
        self.verbose = verbose

    def __call__(
            self,
            dataset,
    ):
        dataloader = DataLoader(dataset, batch_size=self.batch_size)

        hessian_comp = hessian(self.model_orig, self.criterion, dataloader=dataloader, cuda=self.use_cuda)
        top_eigenvalues, top_eigenvector = hessian_comp.eigenvalues(top_n=2)

        num_trial = len(self.lams)
        losses = torch.zeros(size=(num_trial, num_trial))

        for lam1 in tqdm.trange(
                num_trial,
                desc=f"Performing Hessian test...",
                disable=not self.verbose,
        ):
            self.model_pert1 = self.perturb_model(
                self.model_orig, self.model_pert1, top_eigenvector[0], self.lams[lam1]
            )

            for lam2 in range(num_trial):
                self.model_pert2 = self.perturb_model(
                    self.model_pert1, self.model_pert2, top_eigenvector[1], self.lams[lam2])

                loss = 0.0

                for (data, targets) in dataloader:
                    if self.use_cuda:
                        data, targets = data.to("cuda"), targets.to("cuda")

                    loss += self.criterion(self.model_pert2(data), targets).item()

                losses[lam1][lam2] = loss

        return losses

    @staticmethod
    def perturb_model(model_orig, model_pert, direction, alpha):
        for m_orig, m_pert, d in zip(model_orig.parameters(), model_pert.parameters(), direction):
            m_pert.data = m_orig.data + alpha * d

        return model_pert

    def plot(
            self,
            losses: torch.Tensor,
            save_to: str,
            alpha: float = 0.8,
            cmap: str = "viridis",
    ) -> None:
        assert len(losses.shape) == 2 and len(losses[0]) == len(self.lams)

        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

        surf = ax.plot_surface(self.lams, self.lams, losses, alpha=alpha, cmap=cmap,
                               linewidth=0, antialiased=False)

        fig.colorbar(surf, shrink=0.5, aspect=5)

        plt.savefig(save_to, dpi=300, bbox_inches="tight", pad_inches=0)
        plt.draw()
        plt.close("all")
