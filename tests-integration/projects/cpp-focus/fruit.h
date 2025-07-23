#ifndef FRUIT_H
#define FRUIT_H

#include <iostream>
#include <string>
#include <vector>

namespace orchard {

template <typename T>
class Fruit {
public:
    Fruit(const std::string& name, T weight)
        : name_(name), weight_(weight) {}

    virtual ~Fruit() = default;

    virtual void print() const {
        std::cout << "Fruit: " << name_ << ", Weight: " << weight_ << std::endl;
    }

    T getWeight() const { return weight_; }
    std::string getName() const { return name_; }

    // Operator overloads with special characters
    friend std::ostream& operator<<(std::ostream& os, const Fruit& fruit); // <<
    Fruit& operator=(const Fruit& other);                                  // =
    Fruit operator*(double factor) const;                                  // *
    bool operator<(const Fruit& other) const;                              // <
    bool operator>(const Fruit& other) const;                              // >
    bool operator&(const Fruit& other) const;                              // &
    bool operator|(const Fruit& other) const;                              // |
    Fruit operator/(double divisor) const;                                 // /
    Fruit& operator[](size_t idx);                                         // []
    Fruit& operator~();                                                    // ~

    // Function with template and angle brackets
    template <typename U>
    void doSomethingWithTemplate(const U& value) {
        std::cout << "doSomethingWithTemplate called with: " << value << std::endl;
    }

    // Function with parentheses, comma, and default argument
    void complicatedFunc(int a, double b = 3.14, const std::string& s = "banana");

    // Function with reference and pointer
    void refAndPtrFunc(int& a, double* b);

    // Function with const, volatile, and noexcept
    void crazySignature(const int a, volatile double b) noexcept;

protected:
    std::string name_;
    T weight_;
    std::vector<Fruit<T>> basket_;
};

template <typename T>
class Citrus : public Fruit<T> {
public:
    Citrus(const std::string& name, T weight, bool isSweet)
        : Fruit<T>(name, weight), isSweet_(isSweet) {}

    void print() const override {
        std::cout << "Citrus: " << this->name_ << ", Weight: " << this->weight_
                  << ", Sweet: " << (isSweet_ ? "Yes" : "No") << std::endl;
    }

    bool isSweet() const { return isSweet_; }

private:
    bool isSweet_;
};

template <typename T>
class Basket {
public:
    void addFruit(Fruit<T>* fruit) {
        fruits_.push_back(fruit);
    }

    void showContents() const {
        std::cout << "Basket contains:" << std::endl;
        for (const auto& fruit : fruits_) {
            fruit->print();
        }
    }

    ~Basket() {
        for (auto fruit : fruits_) {
            delete fruit;
        }
    }

    // Make fruits_ public for direct access in system tests
    std::vector<Fruit<T>*> fruits_;
};

template <typename T>
Fruit<T>* findInBasket(const Basket<T>& basket, const std::string& name) {
    for (const auto& fruit : basket.fruits_) {
        if (fruit->getName() == name) {
            return fruit;
        }
    }
    return nullptr;
}

} // namespace orchard

#endif // FRUIT_H
