from abc import ABC, abstractmethod
from typing import Any

import jijmodeling as jm
import numpy as np
from dimod import (
    BinaryQuadraticModel,
    ConstrainedQuadraticModel,
    DiscreteQuadraticModel,
)
from pyqubo import cpp_pyqubo  # type: ignore

from strangeworks_optimization_models.mps.bqm_converter import mps_to_bqm
from strangeworks_optimization_models.problem_models import (
    AquilaNDArray,
    MPSFile,
    QuboDict,
)


class StrangeworksConverter(ABC):
    model: Any

    @abstractmethod
    def convert(
        model: Any,
    ) -> (
        BinaryQuadraticModel
        | ConstrainedQuadraticModel
        | DiscreteQuadraticModel
        | jm.Problem
        | AquilaNDArray
        | QuboDict
        | MPSFile
        | tuple
    ):
        ...


class StrangeworksBinaryQuadraticModelJiJProblemConverter(StrangeworksConverter):
    def __init__(self, model: BinaryQuadraticModel):
        self.model = model

    def convert(self) -> tuple[jm.Problem, dict[str, np.ndarray], Any]:
        Q = jm.Placeholder("Q", ndim=2)  # Define variable d
        Q.len_at(0, latex="N")  # Set latex expression of the length of d
        x = jm.BinaryVar("x", shape=(Q.shape[0],))  # Define binary variable
        i = jm.Element("i", belong_to=(0, Q.shape[0]))  # Define dummy index in summation
        j = jm.Element("j", belong_to=(0, Q.shape[1]))  # Define dummy index in summation
        problem = jm.Problem("simple QUBO problem")  # Create problem instance
        problem += jm.sum(i, jm.sum(j, Q[i, j] * x[i] * x[j]))  # Add objective function

        qubo = self.model.to_qubo()

        Qmat = np.zeros((self.model.num_variables, self.model.num_variables))
        map = {m: i for i, m in enumerate(self.model.variables)}
        for k, v in qubo[0].items():
            Qmat[map[k[0]], map[k[1]]] = v

        feed_dict = {"Q": Qmat}
        return problem, feed_dict, map


class StrangeworksBinaryQuadraticModelQuboDictConverter(StrangeworksConverter):
    def __init__(self, model: BinaryQuadraticModel):
        self.model = model

    def convert(self) -> QuboDict:
        qubo = {}
        for lin in self.model.linear:
            qubo[(str(lin), str(lin))] = self.model.linear[lin]
        for quad in self.model.quadratic:
            qubo[(str(quad[0]), str(quad[1]))] = self.model.quadratic[quad]
        return QuboDict(qubo)


class StrangeworksMPSBinaryQuadraticModelConverter(StrangeworksConverter):
    def __init__(self, model: MPSFile):
        self.model = model

    def convert(self, alpha=1e5) -> tuple[BinaryQuadraticModel, cpp_pyqubo.Model]:
        return mps_to_bqm(self.model.data, alpha)

    def decode_response(problem, model, response):
        k2i = {k: i for (i, k) in enumerate(model.variables)}

        result = response

        variables = {}

        for k in problem["binary_keys"]:
            variables[k] = result[k2i[k]]
        for k in problem["continuous_keys"]:
            variables[k] = (
                result[k2i[k]] * (problem["continuous_upper"][k] - problem["continuous_lower"][k])
                + problem["continuous_lower"][k]
            )

        return variables


class StrangeworksConverterFactory:
    @staticmethod
    def from_model(model_from: Any, model_to: Any) -> StrangeworksConverter:
        if isinstance(model_from, BinaryQuadraticModel) and model_to == jm.Problem:
            return StrangeworksBinaryQuadraticModelJiJProblemConverter(model=model_from)
        elif isinstance(model_from, BinaryQuadraticModel) and model_to == QuboDict:
            return StrangeworksBinaryQuadraticModelQuboDictConverter(model=model_from)
        elif isinstance(model_from, MPSFile) and model_to == BinaryQuadraticModel:
            return StrangeworksMPSBinaryQuadraticModelConverter(model=model_from)
        else:
            raise ValueError("Unsupported model type")
