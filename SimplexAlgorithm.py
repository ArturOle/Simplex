import numpy as np
import re


class EquationToArray:
    def __init__(self, equations):
        self.equations = equations

    def transform(self):
        pattern = "(\D+\w\d+(\D+))+|(\D+\w\d+)"
        sub = ' '
        array = re.sub(pattern, sub, self.equations)
        array = array.split()
        for i in range(len(array)):
            array[i] = int(array[i])
        return array


class ConstraintsToArrays:
    def __init__(self, constraints, n):
        self.constraints = constraints
        self.num_of_var = n
        self.array = []

    def extract(self):
        self.constraints = self.constraints.split(";")
        print(self.constraints)
        result = self.create(self.constraints)
        return result

    def create(self, constraints):
        for constraint in constraints:
            if constraint == '':
                break
            temp1 = []

            for i in range(self.num_of_var):
                temp1.append(0)

            pattern = "(\d+[*][x]\d+)|(\d+)"
            constraint = re.findall(pattern, constraint)

            for i, tup in enumerate(constraint):
                for j in tup:
                    if j != '':
                        constraint[i] = j

            print(constraint)
            temp2 = temp1[:]
            for i, var in enumerate(constraint):
                if i < 2:
                    i = var.split("*x")

                    x = int(i[1])-1
                    y = int(i[0])

                    temp2[x] = y
                else:
                    temp2.append(int(var))
            print(temp2)
            self.array.append(temp2)
        return self.array


class Simplex:
    def __init__(self, z, constraints, mode="max"):
        self.function = list(z)
        self.constraints = constraints
        self.mode = mode

        self.simplex_tableau = []

        self.standard_form()
        self.initial_fill()
        self.solve()

    def standard_form(self):
        self.equation()
        self.print_constraints()

    def equation(self):
        print("Function to be", self.mode, ": ")
        equation = []
        for i, x in enumerate(self.function):
            equation.append(''.join([str(x), "x", str(i)]))
        equation = ' + '.join(equation)
        print("Z =", equation, "\n")

    def print_constraints(self):
        print("Problem Constraints: ")
        for constraint in self.constraints:
            equation = [[], '']
            for i, x in enumerate(constraint):
                if i == len(constraint)-1:
                    equation[1] = ''.join([" <= ", str(x)])
                else:
                    equation[0].append(''.join([str(x), "x", str(i)]))
            equation[0] = ' + '.join(equation[0])
            print(equation[0] + equation[1])
        print('')

    def initial_fill(self):
        lengths = [len(self.function)]
        for i in self.constraints:
            lengths.append(len(i))

        dimension = max(lengths)

        for i in self.constraints:
            while len(i) <= dimension:
                i.insert(len(i)-1, 0)

        while len(self.function) < dimension:
            self.function.append(0)

        size = len(self.constraints)
        identity = np.identity(size, int).tolist()

        for j, row in enumerate(identity):
            for elem in row:
                self.constraints[j].insert(len(self.constraints[j])-1, elem)

        for constraint in self.constraints:
            self.simplex_tableau.append(constraint)

        for j in range(size+1):
            self.function.insert(len(self.function), 0)

        self.simplex_tableau.append(self.function)

        if self.mode != "min":
            self.simplex_tableau = np.array(self.simplex_tableau, float)
        else:
            self.simplex_tableau = np.array(self.simplex_tableau, float).T

    def solve(self):
        self.iteration()

    def iteration(self):
        pivot_column = np.argmax(self.simplex_tableau[len(self.simplex_tableau) - 1])
        pivot_row = np.argmax(self.simplex_tableau[:-1, pivot_column])

        while np.max(self.simplex_tableau[len(self.simplex_tableau) - 1]) > 0:
            self.show_pivot(pivot_row, pivot_column)
            self.recalculate(pivot_row, pivot_column)
            pivot_column = np.argmax(self.simplex_tableau[len(self.simplex_tableau) - 1])
            pivot_row = np.argmax(self.simplex_tableau[:-1, pivot_column])

        self.show_pivot(pivot_row, pivot_column)
        self.show_result()

    def show_pivot(self, pivot_y, pivot_x):
        print(self.simplex_tableau)
        print("index:  value: ")
        print("({},{})".format(pivot_x, pivot_y), " ", self.simplex_tableau[pivot_y, pivot_x])

    def recalculate(self, pivot_y, pivot_x):
        temp_table = np.copy(self.simplex_tableau)

        for i, row in enumerate(temp_table):
            if i != pivot_y:
                for j in range(len(row)):
                    row[j] = row[j] - (self.simplex_tableau[pivot_y, j]*self.simplex_tableau[i, pivot_x])/self.simplex_tableau[pivot_y, pivot_x]

        temp_table[pivot_y] = temp_table[pivot_y] / temp_table[pivot_y, pivot_x]
        self.simplex_tableau = np.copy(temp_table)

    def show_result(self):
        if self.mode == "min":
            self.simplex_tableau = self.simplex_tableau.T

        print(self.simplex_tableau)

        for i, row in enumerate(self.simplex_tableau[:-1]):
            print("x{}".format(i), row[-1])


if __name__ == "__main__":
    sim = Simplex([9, 12], [[5, 10, 60], [4, 4, 40]], mode="min")
