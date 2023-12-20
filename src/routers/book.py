from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.shemas import Book
from sqlalchemy.exc import NoResultFound
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/api/v1/book",tags=["book"])


@router.get("/all")
async def get_books(session:AsyncSession = Depends(get_async_session)):
    r = await session.execute("SELECT * FROM book INNER JOIN author ON book.id_author = author.id INNER JOIN publisher ON book.id_publisher = publisher.id")
    res_keys = list(r.keys())
    res_values = r.all()
    result = list()
    for book in res_values:
        book = tuple(book)
        book_add = dict(author=dict(),publisher=dict())
        for i,value in enumerate(book):
            if res_keys[i] not in ("id_publisher","id_author","publisher","name","surname","lastname","city"):
                book_add[res_keys[i]] = value
            if res_keys[i] in ("id_publisher","city","publisher"):
                book_add["publisher"][res_keys[i].replace("id_publisher","id")] = value
            if res_keys[i] in ("id_author","name","lastname","surname"):
                book_add["author"][res_keys[i].replace("id_author","id")] = value
        result.append(book_add)
    return \
    {
        "success":True,
        "message":"Книги",
        "data": result
    }


@router.post("/add")
async def add_book(book:Book,session:AsyncSession = Depends(get_async_session)):
    if book.author.id is not None and book.publisher.id is not None:
        if 2000 >= book.year <= 2024:
            try:
                author_exist = await session.execute(f"SELECT id FROM publisher WHERE id = {book.publisher.id}")
                author_exist.one()
                author_exist = await session.execute(f"SELECT id FROM author WHERE id = {book.author.id}")
                author_exist.one()

                await session.execute(f"""
                INSERT INTO book(name, kind, year, id_author, id_publisher) 
                    VALUES (
                        '{book.title}', '{book.kind}', '{book.year}', '{book.author.id}', '{book.publisher.id}'
                    )
                """)
                await session.commit()
                return \
                    {
                        "success": True,
                        "message": "Книга успешна добавлена!"
                    }
            except Exception as e:
                return JSONResponse({"success": False, "error": str(e)}, status_code=400)
        else:
            return JSONResponse({"success": False, "error": "Year more 2024 or year less than 2000"}, status_code=400)
    else:
        return JSONResponse({"success": False, "error": "publisher or author id is null"}, status_code=400)


@router.put("/update")
async def update_book(book:Book,session:AsyncSession = Depends(get_async_session)):
    if book.author.id is not None and book.publisher.id is not None:
        try:
            author_exist = await session.execute(f"SELECT id FROM publisher WHERE id = {book.publisher.id}")
            author_exist.one()
            author_exist = await session.execute(f"SELECT id FROM author WHERE id = {book.author.id}")
            author_exist.one()

            await session.execute(f"""
            UPDATE book SET name = '{book.title}',
                            kind = '{book.kind}', 
                            year = '{book.year}', 
                            id_author = '{book.author.id}', 
                            id_publisher = '{book.publisher.id}' 
            """)
            await session.commit()
            return {"success": True, "message": "Книга успешна обновлена!"}
        except Exception as e:
            return JSONResponse({"success": False, "error": str(e)}, status_code=400)
    else:
        return JSONResponse({"success": False, "error": "publisher or author id is null"}, status_code=400)


@router.delete("/id={id_book}")
async def delete_book(id_:int,session:AsyncSession = Depends(get_async_session)):
    try:
        author_exist = await session.execute(f"SELECT id FROM book WHERE id = {id_}")
        author_exist.one()

        await session.execute(f"DELETE FROM book WHERE id = {id_}")
        await session.commit()
        return \
            {
                "success": True,
                "message": "Книга удалена"
            }
    except NoResultFound as ex:
        return JSONResponse({"success": False, "error": str(ex)}, status_code=404)
