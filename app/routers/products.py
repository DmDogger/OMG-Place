from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination import Page, Params
from starlette.responses import JSONResponse

from app.auth import get_current_seller, get_current_user
from app.core.dependecies.services.product_service import get_product_service
from app.models.users import User as UserModel
from app.schemas import ProductCreate as ProductCreateSchema, ProductOut, Product as ProductSchema, ProductFilter, \
    ResponseModel
from app.services.product_service import ProductService

router = APIRouter(
    prefix='/products',
    tags=['products']
)

@router.get('/', response_model=Page[ProductOut], status_code=200)
async def get_products(product_service:ProductService = Depends(get_product_service),
                       product_filter: ProductFilter = FilterDepends(ProductFilter),
                       params: Params = Depends()):
    """
    Returns a list of filtered or paginated products.
    """
    products = await product_service.get_filtered_products(product_filter, params)
    return products


@router.get("/search/{product_id}", response_model=ResponseModel[ProductSchema], status_code=200)  ###### refactoring --->
async def get_product(product_id: int,
                      product_service: ProductService = Depends(get_product_service)):
    """
    Returns a product by ID.
    """
    product = await product_service.find_active_product(product_id)
    return ResponseModel(status='success',
                         data=product)

@router.post('/',response_model=ResponseModel[ProductSchema], status_code=201)
async def create_product(product: ProductCreateSchema,
                         current_user: UserModel = Depends(get_current_seller),
                         product_service: ProductService = Depends(get_product_service)):
    """
    Add a new product. Available only for users with role 'seller'.
    """
    product = await product_service.create_product(product, current_user)
    return ResponseModel(status='success',
                         data=product)

@router.get('/search/{category_id}', response_model=list[ProductSchema])
async def get_products_by_category(category_id: int,
                                   product_service: ProductService = Depends(get_product_service)):
    """
    Returns a list of products by category ID.
    """
    products = await product_service.find_products_by_category(category_id)
    return products

@router.put('/{product_id}', response_model=ResponseModel[ProductSchema], status_code=200)
async def update_product(product_id: int,
                         product_data: ProductCreateSchema,
                         user: UserModel = Depends(get_current_user),
                         product_service: ProductService = Depends(get_product_service)
                         ):
    """ Updating product by ID """
    product = await product_service.update_product(product_id, product_data, user)
    return ResponseModel(status='success',
                         data=product)

@router.delete("/{product_id}", status_code=200)
async def delete_product(product_id: int,
                         user: UserModel = Depends(get_current_user),
                         product_service: ProductService = Depends(get_product_service)):
    """
    Delete product by ID.
    """
    await product_service.delete_product(product_id, user)
    return {'message':f'product with id {product_id} has been deleted'}

