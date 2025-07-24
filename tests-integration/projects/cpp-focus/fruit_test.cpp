#include <gtest/gtest.h>
#include <lobster_gtest.h>
#include "fruit.h"

using namespace orchard;

TEST(FruitTest, BasicProperties)
{
    LOBSTER_TRACE("fruits.Clear_Basket");
    Fruit<double> apple("Apple", 150.0);
    EXPECT_EQ(apple.getName(), "Apple");
    EXPECT_DOUBLE_EQ(apple.getWeight(), 150.0);
}

TEST(CitrusTest, Sweetness)
{
    LOBSTER_TRACE("fruits.Clear_Basket");
    Citrus<double> orange("Orange", 120.5, true);
    Citrus<double> lemon("Lemon", 100.0, false);

    EXPECT_TRUE(orange.isSweet());
    EXPECT_FALSE(lemon.isSweet());
    EXPECT_EQ(orange.getName(), "Orange");
    EXPECT_EQ(lemon.getName(), "Lemon");
}

TEST(BasketTest, AddAndShowContents)
{
    Basket<double> basket;
    basket.addFruit(new Fruit<double>("Apple", 150.0));
    basket.addFruit(new Citrus<double>("Orange", 120.5, true));
    basket.addFruit(new Citrus<double>("Lemon", 100.0, false));

    // Check basket contents
    EXPECT_EQ(basket.fruits_.size(), 3);
    EXPECT_EQ(basket.fruits_[0]->getName(), "Apple");
    EXPECT_EQ(basket.fruits_[1]->getName(), "Orange");
    EXPECT_EQ(basket.fruits_[2]->getName(), "Lemon");

    // Just check basket can show contents without crashing
    EXPECT_NO_THROW(basket.showContents());
}

TEST(BasketTest, ClearBasket)
{
    LOBSTER_TRACE("fruits.Sweet_Banana");
    Basket<std::string> basket;
    basket.addFruit(new Fruit<std::string>("Banana", "120"));
    basket.addFruit(new Fruit<std::string>("Apple", "150"));
    EXPECT_EQ(basket.fruits_.size(), 2);

    // Clear basket
    while (!basket.fruits_.empty()) {
        delete basket.fruits_.back();
        basket.fruits_.pop_back();
    }
    EXPECT_EQ(basket.fruits_.size(), 0);
}

TEST(BasketTest, FindInBasketTemplate)
{
    LOBSTER_TRACE("fruits.Fruit_Insertion_Operator");
    Basket<std::string> basket;
    basket.addFruit(new Fruit<std::string>("Banana", "120"));
    basket.addFruit(new Fruit<std::string>("Apple", "150"));

    Fruit<std::string>* found = findInBasket<std::string>(basket, "Banana");
    EXPECT_NE(found, nullptr);
    EXPECT_EQ(found->getName(), "Banana");

    Fruit<std::string>* notFound = findInBasket<std::string>(basket, "Orange");
    EXPECT_EQ(notFound, nullptr);
}
