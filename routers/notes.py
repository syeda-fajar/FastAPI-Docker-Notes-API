from database import engine,get_db
from models import NoteTable
from fastapi import Depends,APIRouter,status,HTTPException
from sqlalchemy.orm import Session
from oauth import get_current_user,OAuth2
from schemas import NoteModel
router =APIRouter(
     prefix="/notes",
     tags=["Notes"]
)

@router.get("/")
async def getNote(db: Session = Depends(get_db),current_user:int =Depends(get_current_user)):
          item=db.query(NoteTable).filter(NoteTable.user_id == current_user).all()
          return item
        

@router.post("/")
async def addNote(notes:NoteModel,db: Session = Depends(get_db),current_user: int = Depends(get_current_user)):
     new_note = NoteTable(title=notes.title, content=notes.content,user_id=current_user)
     db.add(new_note)
     db.commit()
     db.refresh(new_note)
     return new_note

@router.delete("/{notes_id}")
async def DeleteNotes(notes_id:int,db: Session = Depends(get_db),current_user: int = Depends(get_current_user)):
      item = db.query(NoteTable).filter(NoteTable.id == notes_id).first()
      if not item:
       raise HTTPException(status_code=404, detail="Not found")

      if item.user_id != current_user:
        raise HTTPException(status_code=403, detail="Not authorized to perform action")
      db.delete(item)
      db.commit()
      return {"message": "Deleted"}

@router.put("/{notes_id}")
async def UpdateNote(notes_id:int,notes:NoteModel,db:Session=Depends(get_db),current_user: int = Depends(get_current_user)):
       item=db.query(NoteTable).filter(NoteTable.id == notes_id).first()
       if not item:
            raise HTTPException(status_code=404, detail="Item not found")
       if item.user_id != current_user:
        raise HTTPException(status_code=403, detail="Not authorized to update this note")
       item.title =notes.title
       item.content=notes.content
       db.commit()
       db.refresh(item)
       return {"message": "Updated", "note": item}   

      

      
      

     
     