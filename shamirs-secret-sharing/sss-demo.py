import random


def curve(x, coefficients):
	return coefficients[1]*x + coefficients[0]


def create_random_coefficients(k):
	coefficients = []
	for i in range(0, k):
		coefficients.append(random.uniform(-10, 10))

	return coefficients


def get_random_shares(n, coefficients):
	shares = []
	for i in range(0, n):
		x_value = random.uniform(0, 5)
		y_value = curve(x_value, coefficients)

		shares.append([x_value, y_value])

	return shares


def bring_shares_together(shares):
	return ((-1*shares[1][0])/(shares[0][0]-shares[1][0]))*shares[0][1] + \
		((-1*shares[0][0])/(shares[1][0]-shares[0][0]))*shares[1][1]


if __name__ == "__main__":
	coefficients = create_random_coefficients(2)
	print("\nPolynomial:", coefficients[1], "x +", coefficients[0])
	print("Secret Key:", coefficients[0])

	shares = get_random_shares(4, coefficients)
	print("\nRandom Shares:")
	for i in range(0, len(shares)):
		print(i, ":", shares[i])
	print('\n')

	for i in range(0, len(shares)):
		for j in range(i+1, len(shares)):
			print("Share", i, "and", j)
			print(bring_shares_together([shares[i], shares[j]]))
	print('\n')