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
        print(array)
        return array


class ConstraintsToArrays:
    def __init__(self, constraints, n):
        self.constraints = constraints
        self.num_of_var = n
        self.array = []

    def extract(self):
        self.constraints = self.constraints.split(";")
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

            temp2 = temp1[:]
            for i, var in enumerate(constraint):
                if i < 2:
                    i = var.split("*x")

                    x = int(i[1])-1
                    y = int(i[0])

                    temp2[x] = y
                else:
                    temp2.append(int(var))

            self.array.append(temp2)
        print(self.array)
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
            self.recalculate(pivot_row, pivot_column)
            pivot_column = np.argmax(self.simplex_tableau[len(self.simplex_tableau) - 1])
            pivot_row = np.argmax(self.simplex_tableau[:-1, pivot_column])

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

        with open("result.txt", 'w+') as f:
            for i, row in enumerate(self.simplex_tableau):
                np.savetxt(f, row)

        for i, row in enumerate(self.simplex_tableau[:-1]):
            print("x{}".format(i), row[-1])


if __name__ == "__main__":
    eq = EquationToArray(
        "35*x1 + 26*x2 + 24*x3 + 27*x4 + 30*x5 + 17*x6 + 1*x7 + 18*x8 + 31*x9 + 9*x10 + 13*x11 + 13*x12 + 15*x13 + 14*x14 + 20*x15 + 29*x16 + 32*x17 + 14*x18 + 26*x19 + 19*x20 + 31*x21 + 31*x22 + 15*x23 + 15*x24 + 28*x25 + 6*x26 + 26*x27 + 19*x28 + 2*x29 + 27*x30 + 7*x31 + 30*x32 + 17*x33 + 13*x34 + 16*x35 + 31*x36 + 33*x37 + 11*x38 + 30*x39 + 31*x40 + 3*x41 + 34*x42 + 10*x43 + 17*x44 + 14*x45 + 28*x46 + 23*x47 + 29*x48 + 5*x49 + 30*x50 + 14*x51 + 17*x52 + 7*x53 + 15*x54 + 14*x55 + 5*x56 + 32*x57 + 25*x58 + 17*x59 + 21*x60 + 1*x61 + 15*x62 + 24*x63 + 27*x64 + 20*x65 + 19*x66 + 28*x67 + 23*x68 + 12*x69 + 8*x70 + 34*x71 + 4*x72 + 3*x73 + 1*x74 + 27*x75 + 33*x76 + 13*x77 + 22*x78 + 31*x79 + 3*x80 + 3*x81 + 8*x82 + 27*x83 + 27*x84 + 3*x85 + 14*x86 + 20*x87 + 11*x88 + 34*x89 + 23*x90 + 34*x91 + 7*x92 + 19*x93 + 15*x94 + 8*x95 + 12*x96 + 1*x97 + 7*x98 + 11*x99 + 6*x100;").transform()
    cons = ConstraintsToArrays(
        "7*x1 + 7*x51 <= 7;16*x2 + 10*x52 <= 80;15*x3 + 41*x53 <= 100;41*x4 + 26*x54 <= 40;21*x5 + 37*x55 <= 22;41*x6 + 43*x56 <= 33;22*x7 + 18*x57 <= 85;23*x8 + 6*x58 <= 99;7*x9 + 11*x59 <= 84;26*x10 + 30*x60 <= 13;15*x11 + 15*x61 <= 53;36*x12 + 40*x62 <= 88;37*x13 + 24*x63 <= 36;10*x14 + 12*x64 <= 9;31*x15 + 27*x65 <= 67;38*x16 + 39*x66 <= 79;22*x17 + 40*x67 <= 49;31*x18 + 26*x68 <= 6;32*x19 + 6*x69 <= 55;22*x20 + 11*x70 <= 96;5*x21 + 26*x71 <= 28;6*x22 + 25*x72 <= 69;50*x23 + 23*x73 <= 3;40*x24 + 17*x74 <= 66;10*x25 + 45*x75 <= 73;30*x26 + 5*x76 <= 83;27*x27 + 41*x77 <= 90;37*x28 + 2*x78 <= 29;37*x29 + 4*x79 <= 1;6*x30 + 24*x80 <= 46;46*x31 + 10*x81 <= 88;10*x32 + 2*x82 <= 70;44*x33 + 25*x83 <= 84;9*x34 + 45*x84 <= 77;38*x35 + 25*x85 <= 96;21*x36 + 36*x86 <= 87;42*x37 + 25*x87 <= 89;15*x38 + 25*x88 <= 52;14*x39 + 18*x89 <= 87;10*x40 + 34*x90 <= 78;7*x41 + 11*x91 <= 11;29*x42 + 38*x92 <= 34;4*x43 + 17*x93 <= 35;47*x44 + 15*x94 <= 85;36*x45 + 41*x95 <= 90;3*x46 + 15*x96 <= 53;35*x47 + 5*x97 <= 43;21*x48 + 49*x98 <= 93;49*x49 + 48*x99 <= 12;21*x50 + 1*x100 <= 98;",
        n=100)
    sim = Simplex(eq, cons.extract(), mode="min")

