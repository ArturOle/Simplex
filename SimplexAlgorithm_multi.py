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
    eq = EquationToArray("23*x1 + 22*x2 + 29*x3 + 3*x4 + 33*x5 + 24*x6 + 21*x7 + 25*x8 + 18*x9 + 3*x10 + 1*x11 + 3*x12 + 11*x13 + 26*x14 + 13*x15 + 34*x16 + 22*x17 + 4*x18 + 14*x19 + 28*x20 + 20*x21 + 25*x22 + 17*x23 + 16*x24 + 28*x25 + 27*x26 + 29*x27 + 23*x28 + 8*x29 + 27*x30 + 21*x31 + 23*x32 + 17*x33 + 1*x34 + 22*x35 + 22*x36 + 30*x37 + 33*x38 + 24*x39 + 10*x40 + 34*x41 + 18*x42 + 31*x43 + 29*x44 + 5*x45 + 33*x46 + 17*x47 + 25*x48 + 10*x49 + 16*x50 + 5*x51 + 5*x52 + 5*x53 + 3*x54 + 15*x55 + 13*x56 + 28*x57 + 7*x58 + 26*x59 + 24*x60 + 20*x61 + 16*x62 + 33*x63 + 1*x64 + 23*x65 + 24*x66 + 25*x67 + 30*x68 + 20*x69 + 6*x70 + 5*x71 + 32*x72 + 15*x73 + 7*x74 + 14*x75 + 12*x76 + 13*x77 + 33*x78 + 13*x79 + 29*x80 + 15*x81 + 31*x82 + 30*x83 + 3*x84 + 21*x85 + 1*x86 + 30*x87 + 22*x88 + 13*x89 + 35*x90 + 26*x91 + 5*x92 + 30*x93 + 31*x94 + 34*x95 + 26*x96 + 16*x97 + 10*x98 + 33*x99 + 24*x100").transform()
    cons = ConstraintsToArrays("4*x1 + 8*x51 <= 69;36*x2 + 26*x52 <= 83;34*x3 + 33*x53 <= 39;37*x4 + 33*x54 <= 85;15*x5 + 13*x55 <= 42;37*x6 + 44*x56 <= 88;22*x7 + 17*x57 <= 20;33*x8 + 40*x58 <= 32;34*x9 + 6*x59 <= 7;36*x10 + 10*x60 <= 89;50*x11 + 49*x61 <= 9;15*x12 + 32*x62 <= 71;46*x13 + 42*x63 <= 26;22*x14 + 22*x64 <= 51;30*x15 + 5*x65 <= 62;5*x16 + 28*x66 <= 27;22*x17 + 2*x67 <= 6;12*x18 + 48*x68 <= 54;20*x19 + 38*x69 <= 34;2*x20 + 17*x70 <= 5;3*x21 + 5*x71 <= 58;42*x22 + 27*x72 <= 25;5*x23 + 30*x73 <= 1;28*x24 + 42*x74 <= 80;21*x25 + 27*x75 <= 46;10*x26 + 4*x76 <= 12;20*x27 + 25*x77 <= 47;45*x28 + 44*x78 <= 16;46*x29 + 45*x79 <= 67;42*x30 + 50*x80 <= 45;11*x31 + 5*x81 <= 100;3*x32 + 46*x82 <= 86;29*x33 + 34*x83 <= 72;21*x34 + 20*x84 <= 42;21*x35 + 1*x85 <= 97;36*x36 + 20*x86 <= 77;23*x37 + 23*x87 <= 14;11*x38 + 28*x88 <= 91;35*x39 + 38*x89 <= 28;30*x40 + 17*x90 <= 67;3*x41 + 32*x91 <= 73;8*x42 + 50*x92 <= 33;14*x43 + 21*x93 <= 5;4*x44 + 47*x94 <= 78;17*x45 + 9*x95 <= 85;13*x46 + 21*x96 <= 46;20*x47 + 10*x97 <= 35;22*x48 + 24*x98 <= 93;45*x49 + 12*x99 <= 42;12*x50 + 40*x100 <= 37;", n=100)
    sim = Simplex(eq, cons.extract(), mode="min")

