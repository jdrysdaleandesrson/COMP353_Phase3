from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select

engine = create_engine(f"postgresql+psycopg2://postgres:{pwd}@localhost/Test")

class Base(DeclarativeBase):
    pass


class Manager(Base):
    __tablename__ = "IT_manager"
    
    managerID: Mapped[int] = mapped_column(primary_key=True)
    managerFName: Mapped[str] = mapped_column(String(30))
    managerLName: Mapped[str] = mapped_column(String(30))
    managerSalary: Mapped[int] = mapped_column()
    managedDName: Mapped[str] = mapped_column(String(30))
        
    specialists: Mapped[List["Specialist"]] = relationship(
        back_populates="manager", cascade="all, delete-orphan"
    )
    department: Mapped["Department"] = relationship(back_populates="manager")

    
    def __repr__(self) -> str: #represents the object as a string 
        return f"""Manager(managerID={self.managerID!r}, managerFName={self.managerFName!r}, managerLName={self.managerLName!r}, 
    managerSalary={self.managerSalary!r}, managedDName={self.managedDName!r})"""
    
    
class Specialist(Base):
    __tablename__ = "IT_specialist"
    
    specialistID: Mapped[int] = mapped_column(primary_key=True)
    specialistFName: Mapped[str] = mapped_column(String(30))
    specialistLName: Mapped[str] = mapped_column(String(30))
    specialistSalary: Mapped[int] = mapped_column()    
    
    managerID: Mapped[int] = mapped_column(ForeignKey("IT_manager.managerID"))
    
    manager: Mapped["Manager"] = relationship(back_populates="specialists")
    
    def __repr__(self) -> str:
        return f"""Specialist(specialistID={self.specialistID!r}, specialistFName={self.specialistFName!r},specialistLName={self.specialistLName!r},
    specialistSalary={self.specialistSalary!r})"""
    
class Department(Base):
    __tablename__ = "IT_department"
    
    departmentName: Mapped[int] = mapped_column(primary_key=True)
    
    managerID: Mapped[int] = mapped_column(ForeignKey("IT_manager.managerID"))
    manager: Mapped["Manager"] = relationship(back_populates="department")

    
# Drop existing tables
Base.metadata.drop_all(engine)

# Create new tables with the updated schema
Base.metadata.create_all(engine)

#Insert Data
with Session(engine) as session:
    Marquinhos = Manager(
        managerID = '00008554676',
        managerFName='Marquinhos',
        managerLName='Correa',
        managerSalary='155000',
        managedDName= 'Classroom Tech',
        specialists=[Specialist(managerID='00001387051',specialistFName='Roberto',specialistLName='Carlos',specialistSalary='43000'),
                     Specialist(managerID='00002312829',specialistFName='Juan',specialistLName='Felix',specialistSalary='83000'),
                     Specialist(managerID='00006106639',specialistFName='Vinicius',specialistLName='Oliveira',specialistSalary='48000'),
                     Specialist(managerID='00008518764',specialistFName='Thiago',specialistLName='Silva',specialistSalary='77000')],
    )
    Raphinha = Manager(
        managerID = '00003489894',
        managerFName='Raphinha',
        managerLName='Belloli',
        managerSalary='77000',
        managedDName= 'Desktop Services' ,
        specialists=[Specialist(specialistID='00002130529',specialistFName='Richarlison',specialistLName='Andrade',specialistSalary='43000'),
                     Specialist(specialistID='00006969520',specialistFName='Lucas',specialistLName='Paqueta',specialistSalary='100000')],
    )
    Classroom_Tech = Department(departmentName='Classroom Tech')
    Desktop_Services=Department(departmentName='Desktop Services')
    session.add_all([Marquinhos,Raphinha])
    session.commit()

session = Session(engine)  

#Select specialist who work for a manager that works is classroom tech department and earn more than 50000
stmt = select(Specialist).where(Manager.managedDName == "Classroom Tech", Manager.managerID == Specialist.managerID,
                                Specialist.specialistSalary >50000)
for Specialist in session.scalars(stmt): #Execute stmt and return the results as scalars
    print(Specialist)
