class Calculator:
    """
    A class representing a basic calculator with memory functionality.
    """

    def __init__(self):
        """
        Initializes the Calculator object with memory set to 0.
        """
        self.memory = 0

    def add(self, x, y):
        """
        Adds two numbers and updates the memory.

        Args:
            x (float): The first number.
            y (float): The second number.

        Returns:
            float: The result of the addition.
        """
        self.memory = x + y
        return self.memory
        
    def subtract(self, x, y):
        """
        Subtracts the first number from the second one and updates the memory.

        Args:
            x (float): The first number.
            y (float): The second number.

        Returns:
            float: The result of the subtraction.
        """
        self.memory = x - y
        return self.memory

    def multiply(self, x, y):
        """
        Multiplies two numbers and updates the memory.

        Args:
            x (float): The first number.
            y (float): The second number.

        Returns:
            float: The result of the multiplication.
        """
        self.memory = x * y
        return self.memory

    def divide(self, x, y):
        """
        Divides the first number by the second one and updates the memory.

        Args:
            x (float): The first number.
            y (float): The second number.

        Returns:
            float: The result of the division.
        
        Raises:
            ValueError: If the second number is 0.
        """
        if y == 0:
            raise ValueError("Division by zero is not allowed.")
        self.memory = x / y
        return self.memory

    def power(self, x, y):
        """
        Raises the first number to the nth power (the value of the second number) and updates the memory.

        Args:
            x (float): The first number.
            y (float): The second number.

        Returns:
            float: The result of the exponentiation.
        """
        self.memory = x ** y
        return self.memory
    
    def root(self, x, y):
        """
        Calculates the y-th root of the number x without using external libraries.
        Supports complex numbers for negative bases and even exponents.

        Args:
            x (float): The number to extract the root from.
            y (float): The degree of the root.

        Returns:
            float: The result of the root operation rounded to four decimal places.
        """
        # We set the tolerance for convergence
        epsilon = 1e-10
        
        # We initialize the initial root approximation
        guess = 1.0 if x > 1 else x
        
        # Iterate until we get a reasonably accurate approximation of the root
        while abs(guess ** y - x) > epsilon:
            # We update the approximation using the Newton-Raphson method
            guess = ((y - 1) * guess + x / (guess ** (y - 1))) / y
        
        # Round the result to five decimal places
        self.memory = round(guess, 5)
        return self.memory
        
    def reset_memory(self):
        """
        Resets the calculator's memory to 0.
        """
        self.memory = 0

    def perform_operation(self):
        """
        Allows user interaction to perform various operations.
        """
        print("Select operation:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Power")
        print("6. Root")

        while True:
            choice = input("Enter choice(1/2/3/4/5/6): ")

            if choice in ('1', '2', '3', '4', '5', '6'):
                try:
                    num1 = float(input("Enter first number: "))
                    num2 = float(input("Enter second number: "))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue

                if choice == '1':
                    print(num1, "+", num2, "=", self.add(num1, num2))
                elif choice == '2':
                    print(num1, "-", num2, "=", self.subtract(num1, num2))
                elif choice == '3':
                    print(num1, "*", num2, "=", self.multiply(num1, num2))
                elif choice == '4':
                    try:
                        print(num1, "/", num2, "=", self.divide(num1, num2))
                    except ValueError as e:
                        print(e)
                elif choice == '5':
                    print(num1, "^", num2, "=", self.power(num1, num2))
                elif choice == '6':
                    print(num1, "√", num2, "=", self.root(num1, num2))

                next_calculation = input("Let's do the next calculation? (yes/no): ")
                if next_calculation.lower() != "yes":
                    # MEMORY RESET
                    self.reset_memory()
                    break
            else:
                print("Invalid Input")

if __name__ == "__main__":
    calc = Calculator()
    calc.perform_operation()