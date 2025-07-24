/* This is a file that was designed to be used in the context of an integration test.
   The goal here is to use many different C++ features, including templates, operator overloads,
   and various function signatures that include special characters.

   This file serves as a test input for lobster-cpp and lobster-gtest.
*/

#include "fruit.h"
#include <iostream>
#include <string>

using namespace orchard;

// Operator overloads and special functions for Fruit

std::ostream& operator<<(std::ostream& os, const Fruit<double>& fruit) {
    // lobster-trace: fruits.Fruit_Insertion_Operator, fruits.Magic
    os << "Fruit: " << fruit.getName() << ", Weight: " << fruit.getWeight();
    return os;
}

template<>
Fruit<double>& Fruit<double>::operator=(const Fruit<double>& other) {
    // lobster-trace: fruits.Fruit_Copy_Constructor
    // lobster-trace: fruits.SameLine1, fruits.SameLine2, fruits.SameLine3, fruits.SameLine4
    //                fruits.NextLineNotSupported
    if (this != &other) {
        name_ = other.name_;
        weight_ = other.weight_;
    }
    return *this;
}

template<>
Fruit<double> Fruit<double>::operator*(double factor) const {
    // lobster-trace: 123, 456, 89, ab-123, cd-456
    return Fruit<double>(name_, weight_ * factor);
}


template<>
bool Fruit<double>::operator<(const Fruit<double>& other) const {
    return weight_ < other.weight_;
}

template<>
bool Fruit<double>::operator>(const Fruit<double>& other) const {
    return weight_ > other.weight_;
}

template<>
bool Fruit<double>::operator&(const Fruit<double>& other) const {
    return (weight_ > 0) && (other.weight_ > 0);
}

template<>
bool Fruit<double>::operator|(const Fruit<double>& other) const {
    return (weight_ > 0) || (other.weight_ > 0);
}

template<>
Fruit<double> Fruit<double>::operator/(double divisor) const {
    return Fruit<double>(name_, weight_ / divisor);
}

template<>
Fruit<double>& Fruit<double>::operator[](size_t idx) {
    return *this;
}

template<>
Fruit<double>& Fruit<double>::operator~() {
    return *this;
}

/*
// This is a function in a comment:

template<>
Fruit<double>& Fruit<double>::operator~() {
    return *this;
}

*/

template<>
void Fruit<double>::complicatedFunc(int a, double b, const std::string& s) {
    std::cout << "complicatedFunc called with: " << a << ", " << b << ", " << s << std::endl;
}

template<>
void Fruit<double>::refAndPtrFunc(int& a, double* b) {
    std::cout << "refAndPtrFunc called with: " << a << ", " << (b ? *b : 0) << std::endl;
}

template<>
void Fruit<double>::crazySignature(const int a, volatile double b) noexcept {
    std::cout << "crazySignature called with: " << a << ", " << b << std::endl;
}

void buyBanana(Basket<double>& basket) {
    // lobster-trace: fruits.Buy_Banana1
    // lobster-trace: fruits.Buy_Banana2
    basket.addFruit(new Fruit<double>("Banana", 120.5));
    std::cout << "Added one banana to the basket." << std::endl;
}

void sellBanana(Basket<double>& basket) {
    // lobster-trace: fruits.Sell_Banana1
    // lobster-trace: fruits.Sell_Banana2
    for (auto it = basket.fruits_.begin(); it != basket.fruits_.end(); ++it) {
        if ((*it)->getName() == "Banana") {
            delete *it;
            basket.fruits_.erase(it);
            std::cout << "Sold one banana from the basket." << std::endl;
            return;
        }
    }
    std::cout << "No banana to sell." << std::endl;
}

void clearBasket(Basket<double>& basket) {
    // lobster-trace: fruits.Clear_Basket
    while (!basket.fruits_.empty()) {
        delete basket.fruits_.back();
        basket.fruits_.pop_back();
    }
    std::cout << "Cleared the basket." << std::endl;
}

void checkBasket(Basket<double>& basket) {
    // lobster-trace: fruits.Check_Basket
    int count = 0;
    for (const auto& fruit : basket.fruits_) {
        if (fruit->getName() == "Banana") {
            ++count;
        }
    }
    std::cout << "Basket contains " << count << " bananas." << std::endl;
}

void throwBanana(Basket<double>& basket) {
    // lobster-trace: fruits.Throw_Banana
    for (auto it = basket.fruits_.begin(); it != basket.fruits_.end(); ++it) {
        if ((*it)->getName() == "Banana") {
            delete *it;
            basket.fruits_.erase(it);
            std::cout << "Threw the banana away." << std::endl;
            return;
        }
    }
    std::cout << "No banana to throw away." << std::endl;
}

int main() {
    Basket<double> basket;
    buyBanana(basket);
    checkBasket(basket);
    sellBanana(basket);
    checkBasket(basket);
    buyBanana(basket);
    throwBanana(basket);
    checkBasket(basket);
    clearBasket(basket);
    checkBasket(basket);

    // Use the templated function (name will contain <double>)
    Fruit<double>* found = findInBasket<double>(basket, "Banana");
    if (found) {
        std::cout << "Found a banana in the basket." << std::endl;
    } else {
        std::cout << "No banana found in the basket." << std::endl;
    }

    // Use the templated function (name will contain <int>)
    Fruit<int> apple("Apple", -150);
    apple.doSomethingWithTemplate<int>(42);


    return 0;
}
