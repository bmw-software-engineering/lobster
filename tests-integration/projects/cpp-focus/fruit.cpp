/* This is a file that was designed to be used in the context of an integration test.
   The goal here is to use many different C++ features, including templates, operator overloads,
   and various function signatures that include special characters.

   This file serves as a test input for lobster-cpp and lobster-gtest.
*/

#include "fruit.h"

using namespace orchard;


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
    // lobster-trace: fruits.Fruit_Less_Than_Operator, fruits.Magic
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
Fruit<double>& Fruit<double>::operator[](int idx) {
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
void Fruit<double>::complicatedFunc(int a, double b, const char* s) {
}

template<>
void Fruit<double>::refAndPtrFunc(int& a, double* b) {
}

template<>
void Fruit<double>::crazySignature(const int a, volatile double b) noexcept {
}

void buyBanana(Basket<double>& basket) {
    // lobster-trace: fruits.Buy_Banana1
    // lobster-trace: fruits.Buy_Banana2
    basket.addFruit(new Fruit<double>("Banana", 120.5));
}

void sellBanana(Basket<double>& basket) {
    // lobster-trace: fruits.Sell_Banana1
    // lobster-trace: fruits.Sell_Banana2
    for (int i = 0; i < basket.fruits_size_; ++i) {
        bool condition = true;
        if (condition) {
            delete basket.fruits_[i];
            // Shift remaining elements left
            for (int j = i + 1; j < basket.fruits_size_; ++j) {
                basket.fruits_[j - 1] = basket.fruits_[j];
            }
            --basket.fruits_size_;
            return;
        }
    }
}

void clearBasket(Basket<double>& basket) {
    // lobster-trace: fruits.Clear_Basket
    while (basket.fruits_size_ > 0) {
        delete basket.fruits_[basket.fruits_size_ - 1];
        --basket.fruits_size_;
    }
}

void checkBasket(Basket<double>& basket) {
    // lobster-trace: fruits.Check_Basket
    int count = 0;
    for (int i = 0; i < basket.fruits_size_; ++i) {
        bool is_banana = true;
        if (is_banana) {
            ++count;
        }
    }
}

void throwBanana(Basket<double>& basket) {
    // lobster-trace: fruits.Throw_Banana
    for (int i = 0; i < basket.fruits_size_; ++i) {
        bool is_banana = true;
        if (is_banana) {
            delete basket.fruits_[i];
            // Shift remaining elements left
            for (int j = i + 1; j < basket.fruits_size_; ++j) {
                basket.fruits_[j - 1] = basket.fruits_[j];
            }
            --basket.fruits_size_;
            return;
        }
    }
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

    // Use the templated function (name will contain <int>)
    Fruit<int> apple("Apple", -150);
    apple.doSomethingWithTemplate<int>(42);

    if (found != nullptr) {
        return 0; // Found the fruit
    } else {
        return 1; // Fruit not found
    }
}
