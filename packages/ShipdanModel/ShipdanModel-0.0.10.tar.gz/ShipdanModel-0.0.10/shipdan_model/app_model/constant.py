# payment
class DietPaymentScheduleStatus:
    UNDEFINED = 0
    REGISTERED = 1
    DIET_CREATE_COMPLETE = 2
    DIET_CREATE_FAILED = 3
    PAYMENT_COMPLETE = 4
    PAYMENT_FAILED = 5
    SKIP = 6
    PAYMENT_CANCEL = 7
    CANCEL = -1


DIET_PAYMENT_SCHEDULE_STATUS = (
    (DietPaymentScheduleStatus.UNDEFINED, '미정'),
    (DietPaymentScheduleStatus.REGISTERED, '등록'),
    (DietPaymentScheduleStatus.DIET_CREATE_COMPLETE, '식단 생성 성공'),
    (DietPaymentScheduleStatus.DIET_CREATE_FAILED, '식단 생성 실패'),
    (DietPaymentScheduleStatus.PAYMENT_COMPLETE, '결제 성공'),
    (DietPaymentScheduleStatus.PAYMENT_FAILED, '결제 실패'),
    (DietPaymentScheduleStatus.SKIP, '건너뜀'),
    (DietPaymentScheduleStatus.PAYMENT_CANCEL, '결제 취소'),
    (DietPaymentScheduleStatus.CANCEL, '해지'),
)


# health
class FoodProductTasteScoreStatus:
    UNDEFINED = 0
    BAD = 1
    NEUTRAL = 2
    GOOD = 3


FOOD_PRODUCT_TASTE_SCORE_STATUS = (
    (FoodProductTasteScoreStatus.UNDEFINED, '미정'),
    (FoodProductTasteScoreStatus.BAD, '나쁨'),
    (FoodProductTasteScoreStatus.NEUTRAL, '보통'),
    (FoodProductTasteScoreStatus.GOOD, '좋음'),
)


# food_payment
class FoodOrderStatus:
    UNDEFINED = 0
    ORDER_COMPLETE = 1
    PAYMENT_COMPLETE = 2
    DELIVERY_COMPLETE = 3
    CANCEL_ORDER = -10

    FAIL = -20


FOOD_ORDER_STATUS = (
    (FoodOrderStatus.UNDEFINED, '미정'),
    (FoodOrderStatus.ORDER_COMPLETE, '주문완료'),
    (FoodOrderStatus.PAYMENT_COMPLETE, '결제완료'),
    (FoodOrderStatus.DELIVERY_COMPLETE, '배달완료'),
    (FoodOrderStatus.CANCEL_ORDER, '주문취소'),
    (FoodOrderStatus.FAIL, '문제상황'),
)
