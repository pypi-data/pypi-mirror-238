#ifndef SOLVERS_H
#define SOLVERS_H

#include <cmath>
#include <functional>
#include <string>

using namespace std;

namespace Solvers
{

    template <typename Func>
    double new_raph_solve(Func fn, double tgt, double tol = 1e-9, double max_iters = 1e6, double guess = 0.05, double d_eps = 1e-6)
    {
        int n_iter = 0.0;
        while (n_iter <= max_iters)
        {
            double res = fn(guess);
            double diff = res - tgt;
            if (std::abs(diff) < tol)
            {
                return guess;
            }
            double deriv = (fn(guess + d_eps) - fn(guess - d_eps)) / (2 * d_eps);
            guess = guess - diff / deriv;
            n_iter += 1;
        }
        throw("Solver did not converge after " + std::to_string(max_iters) + " iterations");
    }

}

#endif // SOLVERS_H