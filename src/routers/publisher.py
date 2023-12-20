from fastapi import APIRouter,Depends
from src.database import AsyncSession,get_async_session
from src.shemas import Publisher
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound

router = APIRouter(prefix="/api/v1/publisher",tags=["publisher"])


@router.get("/all")
async def get_publishers(session:AsyncSession = Depends(get_async_session)):
    r = await session.execute("SELECT * FROM publisher;")
    return \
        {
            "success": True,
            "message": "Издатели",
            "data": r.all()
        }


@router.post("/add")
async def add_publisher(publisher:Publisher,session:AsyncSession = Depends(get_async_session)):
    try:
        await session.execute(f"INSERT INTO publisher(publisher, city) VALUES('{publisher.publisher}', '{publisher.city}')")
        await session.commit()
        return \
            {
                "success": True,
                "message": "Издатель успешно добавлен!"
            }
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=400)


@router.put("/update")
async def update_publisher(publisher:Publisher,session:AsyncSession = Depends(get_async_session)):
    if publisher.id is not None:
        try:
            author_exist = await session.execute(f"SELECT id FROM publisher WHERE id = {publisher.id}")
            author_exist.one()

            await session.execute(f"UPDATE publisher SET name = '{publisher.publisher}', city = '{publisher.city}' WHERE id = {publisher.id}")
            await session.commit()
            return \
                {
                    "success": True,
                    "message": "Данные изменены"
                }
        except NoResultFound as ex:
            return JSONResponse({"success": False, "error": str(ex)}, status_code=404)
    else:
        return JSONResponse({"success": False, "error": "ID not changed"}, status_code=400)
