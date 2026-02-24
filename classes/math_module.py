from scipy import optimize
# Symbolic Python
from sympy import *
import numpy as np


class MathModule:
    """Provides mathematical computations for inclinometer calibration.
    
    Attributes:
        x (np.ndarray): X coordinates.
        y (np.ndarray): Y coordinates.
    """
    def __init__(self, x, y):
        """Initializes the MathModule with x and y coordinates.
        
        Args:
            x (np.ndarray): Array of X values.
            y (np.ndarray): Array of Y values.
        """
        self.x: np.array = x
        self.y: np.array = y

    def coeff_mat_estimator3(self):
        """Calculates the coefficient matrix for a cubic estimator.
        
        Returns:
            np.ndarray: Evaluated 5x5 matrix.
        """
        A = np.array([[(self.x ** 4).sum(), (self.y * self.x ** 3).sum(), (self.x ** 2 * self.y ** 2).sum(),
                       (self.x ** 3).sum(), (self.x ** 2).sum()],
                      [(self.x ** 3 * self.y).sum(), (self.x ** 2 * self.y ** 2).sum(), (self.x * self.y ** 3).sum(),
                       (self.x ** 2 * self.y).sum(),
                       (self.x * self.y).sum()],
                      [(self.x ** 2 * self.y ** 2).sum(), (self.x * self.y ** 3).sum(), (self.y ** 4).sum(),
                       (self.x * self.y ** 2).sum(), (self.y ** 2).sum()],
                      [(self.x ** 3).sum(), (self.x ** 2 * self.y).sum(), (self.x * self.y ** 2).sum(),
                       (self.x ** 2).sum(), self.x.sum()],
                      [(self.x ** 2).sum(), (self.x * self.y).sum(), (self.y ** 2).sum(), self.x.sum(), self.x.size]])
        return A

    def coeff_mat_estimator2(self):
        """Calculates the coefficient matrix for a quadratic estimator.
        
        Returns:
            tuple: A tuple containing the solution vector X and the residual vector v.
        """
        A = np.array([[(self.x ** 4).sum(), (self.x ** 3).sum(), (self.x ** 2).sum()],
                      [(self.x ** 3).sum(), (self.x ** 2).sum(), self.x.sum()],
                      [(self.x ** 2).sum(), self.x.sum(), 30]])
        L = np.array([(self.y * self.x ** 2).sum(), (self.y * self.x).sum(), self.y.sum()])
        X = np.linalg.solve(A, L)
        v = A.dot(X) - L

        return X, v

    def VIM_parabola_params_est(self):
        """Estimates parabola parameters for VIM calibration.
        
        Returns:
            tuple: Estimated parameters (VIM_parabola_params) and standard errors (ma, mb, mc, md, mf).
        """
        A = np.array([[(self.x ** 4).sum(), (self.y * self.x ** 3).sum(), (self.x ** 2 * self.y ** 2).sum(),
                       (self.x ** 3).sum(), (self.x ** 2).sum()],
                      [(self.x ** 3 * self.y).sum(), (self.x ** 2 * self.y ** 2).sum(), (self.x * self.y ** 3).sum(),
                       (self.x ** 2 * self.y).sum(),
                       (self.x * self.y).sum()],
                      [(self.x ** 2 * self.y ** 2).sum(), (self.x * self.y ** 3).sum(), (self.y ** 4).sum(),
                       (self.x * self.y ** 2).sum(), (self.y ** 2).sum()],
                      [(self.x ** 3).sum(), (self.x ** 2 * self.y).sum(), (self.x * self.y ** 2).sum(),
                       (self.x ** 2).sum(), self.x.sum()],
                      [(self.x ** 2).sum(), (self.x * self.y).sum(), (self.y ** 2).sum(), self.x.sum(), self.x.size]])
        L = np.array(
            [(self.y * self.x ** 2).sum(), (self.x * self.y ** 2).sum(), (self.y ** 3).sum(), (self.x * self.y).sum(),
             self.y.sum()])
        N = np.linalg.inv(A.transpose().dot(A))
        X = N.dot(A.transpose()).dot(L)
        v = A.dot(X) - L
        mu = np.sqrt(v.transpose().dot(v) / 4)
        ma = mu * np.sqrt(N[0, 0])
        mb = mu * np.sqrt(N[1, 1])
        mc = mu * np.sqrt(N[2, 2])
        md = mu * np.sqrt(N[3, 3])
        mf = mu * np.sqrt(N[4, 4])
        VIM_parabola_params = X
        return VIM_parabola_params, ma, mb, mc, md, mf

    # def coeff_mat_estimator2(x: np.array, y: np.array):
    #     A = np.array([[(x ** 4).sum(), (x ** 3).sum(), (x ** 2).sum()],
    #                   [(x ** 3).sum(), (x ** 2).sum(), x.sum()],
    #                   [(x ** 2).sum(), x.sum(), 30]])
    #     return A

    def VIM_calibrated_inklination(VIM_calibration_params: np.array, VIM_parabola_params: np.array):
        """Calculates calibrated inclination based on VIM parameters.
        
        Args:
            VIM_calibration_params (np.ndarray): Calibration parameters.
            VIM_parabola_params (np.ndarray): Parabola parameters.
            
        Returns:
            float | np.ndarray: Calculated inclination.
        """
        inklination = VIM_parabola_params.dot(VIM_calibration_params)
        return inklination
