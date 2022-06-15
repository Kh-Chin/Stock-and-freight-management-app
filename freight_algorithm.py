"""
This file is for the algorithm calculating freight fee based on weight and volume
"""
import math


def small_pack(weight, width, height, length):
    # Calculate price using small_pack algorithm
    m3_kg = width * height * length / 6000
    if m3_kg > weight:
        weight = m3_kg

    first_kg_fee = 17
    if 0 <= weight <= 1:
        small_pack_price = first_kg_fee
        price_id = 1

    elif 1 < weight <= 10:
        small_pack_price = first_kg_fee + (math.ceil(weight) - 1) * 8
        price_id = 1

    elif 10 < weight <= 100:
        small_pack_price = math.ceil(weight) * 7
        price_id = 2

    else:
        small_pack_price = math.ceil(weight) * 6
        price_id = 3

    return small_pack_price, price_id


def big_pack(m3):
    # Calculate price using big_pack algorithm
    first_m3_fee = 210

    if 0 < m3 <= 3:
        big_pack_price = first_m3_fee
        price_id = 4

    elif 3 < m3 < 10:
        big_pack_price = first_m3_fee + (math.ceil(m3) - 3) * 700 / 10
        price_id = 4

    elif 10 <= m3 < 30:
        big_pack_price = math.ceil(m3) * 690 / 10
        price_id = 5

    else:
        big_pack_price = math.ceil(m3) * 680 / 10
        price_id = 6

    return big_pack_price, price_id
