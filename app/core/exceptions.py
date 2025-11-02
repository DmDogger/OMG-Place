from fastapi import HTTPException

class ProductNotFound(HTTPException):
    """
    Ошибка, если товар не найден.
    """
    def __init__(self):
        super().__init__(status_code=404,
                         detail="Product not found")
        self.error_code = 'PRODUCT_NOT_FOUND'

class SellerCannotLeaveReview(HTTPException):
    """
    Ошибка, если продавец пытается оставить отзыв.
    """
    def __init__(self):
        super().__init__(status_code=403,
                         detail="Seller cannot leave a review")
        self.error_code = 'SELLER_CANNOT_LEAVE_REVIEW'

class ReviewNotFound(HTTPException):
    """
    Ошибка, если отзыв не найден.
    """
    def __init__(self):
        super().__init__(status_code=404,
                         detail='Review not found')
        self.error_code = 'REVIEW_NOT_FOUND'

class CanReviewOnlyOnce(HTTPException):
    """
    Ошибка, если отзыв уже оставлен.
    """
    def __init__(self):
        super().__init__(status_code=400,
                         detail='You can review only once')
        self.error_code = 'CAN_REVIEW_ONLY_ONCE'

class CategoryNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404,
                         detail='Category not found')
        self.error_code = 'CATEGORY_NOT_FOUND'

class ProductOwnershipError(HTTPException):
    """
    Ошибка, если товар не принадлежит продавцу.
    """
    def __init__(self):
        super().__init__(status_code=403,
                         detail='You can delete only your own products')
        self.error_code = 'PRODUCT_OWNERSHIP_ERROR'