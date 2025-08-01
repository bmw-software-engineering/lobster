#ifndef FRUIT_H
#define FRUIT_H

namespace orchard {

template <typename T>
class Fruit {
public:
    Fruit(const char* name, T weight)
        : name_(name), weight_(weight), basket_size_(0) {}

    virtual ~Fruit() = default;

    virtual void print() const {
        // print a message
    }

    T getWeight() const { return weight_; }
    const char* getName() const { return name_; }

    // Operator overloads with special characters
    Fruit& operator=(const Fruit& other);                                  // =
    Fruit operator*(double factor) const;                                  // *
    bool operator<(const Fruit& other) const;                              // <
    bool operator>(const Fruit& other) const;                              // >
    bool operator&(const Fruit& other) const;                              // &
    bool operator|(const Fruit& other) const;                              // |
    Fruit operator/(double divisor) const;                                 // /
    Fruit& operator[](int idx);                                         // []
    Fruit& operator~();                                                    // ~

    // Function with template and angle brackets
    template <typename U>
    void doSomethingWithTemplate(const U& value) {
        //std::cout << "doSomethingWithTemplate called with: " << value << std::endl;
    }

    // Function with parentheses, comma, and default argument
    void complicatedFunc(int a, double b = 3.14, const char* s = "banana");

    // Function with reference and pointer
    void refAndPtrFunc(int& a, double* b);

    // Function with const, volatile, and noexcept
    void crazySignature(const int a, volatile double b) noexcept;

protected:
    const char* name_;
    T weight_;
    Fruit<T>* basket_[10];
    int basket_size_;   // track the number of elements manually
};

template <typename T>
class Citrus : public Fruit<T> {
public:
    Citrus(const char* name, T weight, bool isSweet)
        : Fruit<T>(name, weight), isSweet_(isSweet) {}

    void print() const override {
        // print a message
    }

    bool isSweet() const { return isSweet_; }

private:
    bool isSweet_;
};

template <typename T>
class Basket {
public:
void addFruit(Fruit<T>* fruit) {
    if (fruits_size_ < 10) {
        fruits_[fruits_size_++] = fruit;
    }
}

    void showContents() const {
        for (int i = 0; i < fruits_size_; ++i) {
            if (fruits_[i]) {
                fruits_[i]->print();
            }
        }
    }

    ~Basket() {
        for (int i = 0; i < this->fruits_size_; ++i) {
            delete this->fruits_[i];
        }
        this->fruits_size_ = 0;
    }

    Fruit<T>* fruits_[10];
    int fruits_size_ = 0; // track the number of elements
};

template <typename T>
Fruit<T>* findInBasket(const Basket<T>& basket, const char* name) {
    for (int i = 0; i < basket.fruits_size_; ++i) {
        if (basket.fruits_[i]->getName() == name) {
            return basket.fruits_[i];
        }
    }
    return nullptr;
}

} // namespace orchard

#endif // FRUIT_H
