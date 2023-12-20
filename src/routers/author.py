from fastapi import APIRouter,Depends
from src.database import AsyncSession,get_async_session
from src.shemas import Author
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound

router = APIRouter(prefix="/api/v1/author",tags=["author"])


@router.get("/all")
async def get_authors(session:AsyncSession = Depends(get_async_session)):
    r = await session.execute("SELECT * FROM author;")
    return \
        {
            "success": True,
            "message": "Авторы",
            "data": r.all()
        }


@router.post("/add")
async def add_author(author:Author,session:AsyncSession = Depends(get_async_session)):
    try:
        await session.execute(f"INSERT INTO author(name, lastname, surname) VALUES('{author.name}', '{author.lastname}', '{author.surname}')")
        await session.commit()
        return \
            {
                "success":True,
                "message":"Автор успешно добавлен!"
            }
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)},status_code=400)


@router.put("/update")
async def update_author(author:Author,session:AsyncSession = Depends(get_async_session)):
    if author.id is not None:
        try:
            author_exist = await session.execute(f"SELECT id FROM author WHERE id = {author.id}")
            author_exist.one()

            await session.execute(f"UPDATE author SET name = '{author.name}', lastname = '{author.lastname}', surname = '{author.surname}' WHERE id = {author.id}")
            await session.commit()
            return \
                {
                    "success": True,
                    "message": "Данные изменены"
                }
        except NoResultFound as ex:
            return JSONResponse({"success":False,"error":str(ex)},status_code=404)
    else:
        return JSONResponse({"success": False, "error": "ID not changed"}, status_code=400)