import matplotlib.pyplot as plt
import numpy as np

def mobious(x: np.ndarray, theta: float):
    return (np.cos(theta/2)*x - np.sin(theta/2))/(x*np.sin(theta/2) + np.cos(theta/2))

def main():
    num_points = 1000
    num_thetas = 10
    args = np.linspace(start=0, stop=10, num=num_points)
    thetas = np.linspace(start=0, stop=2*np.pi, num=num_thetas)
    for theta in thetas:
        tmp_res = mobious(args, theta)
        plt.plot(args, tmp_res)

    plt.show()

if __name__ == "__main__":
    main()