#ifndef CONFIGS_H
#define CONFIGS_H

struct CalibrationConfig
{
    int max_iter = 1e4;
    double x_tol = 1e-6;

    CalibrationConfig(){};
    CalibrationConfig(int max_iter_, double x_tol_) : max_iter{max_iter_}, x_tol{x_tol} {};
};

#endif // CONFIGS_H