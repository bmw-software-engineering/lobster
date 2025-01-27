/**
  * A simple Scala program demonstrating various features like
  * case classes, objects, methods, and documentation comments.
  */

// Define a case class to represent a Person
case class Person(name: String, age: Int)

/**
  * An object to hold utility methods for greeting and age validation.
  */
object Utilities {

  /**
    * Generates a greeting message for a person.
    *
    * @requirement CB-#0815 CB-#0816
    *
    * @param person The person to greet.
    * @return A greeting string.
    */
  def greet(person: Person): String = {
    s"Hello, ${person.name}! You are ${person.age} years old."
  }

  /**
    * Checks if a person is considered an adult.
    *
    * @requirement CB-#0815, CB-#0816,
    * 				CB-#0817
    * @requirement CB-#0818 CB-#0819
    * 				CB-#0820
    *
    * @param person The person to check.
    * @return True if the person is an adult (18 or older), otherwise false.
    */
  def isAdult(person: Person): Boolean = {
    person.age >= 18
  }
}

/**
  * The main object to run the program.
  */
object Main {

  /**
    * The entry point of the application.
    *
    * @requiredby FOO0::BAR0, FOO1::BAR1,
    * 			   FOO2::BAR2
    * @requiredby FOO3::BAR3 FOO4::BAR4,
    * 			   FOO5::BAR5
    * @requiredby FOO6::BAR6 FOO7::BAR7
    * 			   FOO8::BAR8
    *
    * @param args Command-line arguments (not used in this program).
    */
  def main(args: Array[String]): Unit = {
    val person = Person("Alice", 25)

    // Generate a greeting
    println(Utilities.greet(person))

    // Check if the person is an adult
    if (Utilities.isAdult(person)) {
      println(s"${person.name} is an adult.")
    } else {
      println(s"${person.name} is not an adult.")
    }
  }
}
