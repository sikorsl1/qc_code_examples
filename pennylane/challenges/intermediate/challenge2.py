import json
import pennylane as qml
import pennylane.numpy as np

def maximal_probability(theta_1, theta_2, p_1, p_2):

    """
    This function calculates the maximal probability of distinguishing
    the states

    Args:
        theta_1 (float): Angle parametrizing the state |phi_1>.
        theta_2 (float): Angle parametrizing the state |phi_2>.
        p_1 (float): Probability that the state was |phi_1>.
        p_2 (float): Probability that the state was |phi_2>.

    Returns:
        (Union[float, np.tensor]): Maximal probability of distinguishing the states.
    
    """
    def opt_cost(params):
        v_11 = np.cos(params[0])*np.exp(1j*params[1])
        v_12 = np.sin(params[0])*np.exp(1j*params[2])
        v_21 = -np.sin(params[0])*np.exp(-1j*params[2])
        v_22 = np.cos(params[0])*np.exp(-1j*params[1])
        res = p_1*abs(v_11*np.cos(theta_1) + v_12*np.sin(theta_1))**2 +\
            p_2*abs(v_21*np.cos(theta_2) + v_22*np.sin(theta_2))**2
        return -res
    
    opt = qml.AdagradOptimizer(stepsize=0.1)

    params = np.array([0., 1., 2.])

    print("Initialization: Cost = {:6.4f}".format(opt_cost(params)))
    for i in range(10000):
        params, cost_ = opt.step_and_cost(opt_cost, params)

        if (i + 1) % 100 == 0:
            print(
                "Iteration {:>4}: Cost = {:6.4f}".format(i + 1, cost_)
            )
    print(-cost_)
    return -cost_


    # Put your code here

    # Return the highest probability of distinguishing the states


# These functions are responsible for testing the solution.


def run(test_case_input: str) -> str:
    theta1, theta2, p_1, p_2 = json.loads(test_case_input)
    prob = np.array(maximal_probability(theta1, theta2, p_1, p_2)).numpy()

    return str(prob)


def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)

    assert np.allclose(solution_output, expected_output, rtol=1e-4)


# These are the public test cases
test_cases = [
    ('[0, 0.7853981633974483, 0.25, 0.75]', '0.8952847075210476'),
    ('[1.83259571459, 1.88495559215, 0.5, 0.5]', '0.52616798')
]

# This will run the public test cases locally
for i, (input_, expected_output) in enumerate(test_cases):
    print(f"Running test case {i} with input '{input_}'...")

    try:
        output = run(input_)

    except Exception as exc:
        print(f"Runtime Error. {exc}")

    else:
        if message := check(output, expected_output):
            print(f"Wrong Answer. Have: '{output}'. Want: '{expected_output}'.")

        else:
            print("Correct!")