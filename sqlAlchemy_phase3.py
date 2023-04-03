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
from sqlalchemy import func

pwd = input("password: ")
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

class StudentEmp(Base):
    __tablename__ = "studentEmp"

    studentID: Mapped[str] = mapped_column(primary_key=True)
    studentFName: Mapped[str] = mapped_column(String(50))
    studentLName: Mapped[str] = mapped_column(String(50))
    studentSalary: Mapped[int] = mapped_column()
    processorIssues: Mapped[List["ProcessorIssue"]] = relationship(back_populates="student", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"studentID={self.studentID!r}, studentFName={self.studentFName!r}, studentLName={self.studentLName!r}," \
               f"studentSalary={self.studentSalary!r}"

class ProcessorIssue(Base):
    __tablename__ = "processorIssue"

    caseNum: Mapped[int] = mapped_column(primary_key=True)
    diagnosisDate: Mapped[str] = mapped_column(String(10))
    buildingName: Mapped[str] = mapped_column(String(50))
    partName: Mapped[str] = mapped_column(String(50))

    student_id: Mapped[str] = mapped_column(ForeignKey("studentEmp.studentID"))

    student: Mapped["StudentEmp"] = relationship(back_populates="processorIssues")

    def __repr__(self) -> str: #represents the object as a string
        return f"ProcessorIssue(caseNum = {self.caseNum!r}, diagnosisDate = {self.diagnosisDate!r}," \
               f"buildingName = {self.buildingName!r}, partName = {self.partName!r})"

    
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

    Cindy = StudentEmp(
        studentID='00007810224',
        studentFName='Cindy',
        studentLName='George',
        studentSalary='5000',
        # Cindy casNums = 1, 8, 9, 11
        processorIssues=[ProcessorIssue(caseNum='1', diagnosisDate='01/05/2023', buildingName='Cudahy Science Hall',
                                       partName='HDMI Couplers'),
                        ProcessorIssue(caseNum='8', diagnosisDate='03/19/2023', buildingName='Edward Crown Center',
                                       partName='Audio Extractor'),
                        ProcessorIssue(caseNum='9', diagnosisDate='03/22/2023', buildingName='Cudahy Science Hall',
                                       partName='HDMI Couplers'),
                        ProcessorIssue(caseNum='11', diagnosisDate='04/01/2023', buildingName='Edward Crown Center',
                                       partName='Touch Panel')]
    )
    Barbara = StudentEmp(
        studentID='00005637594',
        studentFName='Barbara',
        studentLName='Wallace',
        studentSalary='5000',
        # Barbara casNums = 2, 7
        processorIssues=[ProcessorIssue(caseNum='2', diagnosisDate='01/09/2023', buildingName='Dumbach Hall',
                                        partName='Shure Microphone Transmitter'),
                         ProcessorIssue(caseNum='7', diagnosisDate='02/21/2023', buildingName='Edward Crown Center',
                                        partName='VGA Couplers')]
    )
    session.add_all([Marquinhos,Raphinha,Cindy,Barbara,Classroom_Tech, Desktop_Services])
    session.commit()

session = Session(engine)  

#specilistSalUnderManager
specilistSalUnderManager = select(func.count(Specialist.specialistID)).where(Manager.managedDName == "Classroom Tech", Manager.managerID == Specialist.managerID,
                                Specialist.specialistSalary >50000)
for Specialist in session.scalars(specilistSalUnderManager): 
    print("specilistSalUnderManager: " + str(Specialist))

session = Session(engine)
stmt = select(StudentEmp.studentFName, StudentEmp.studentLName, func.count(ProcessorIssue.caseNum))\
    .join(StudentEmp.processorIssues)\
    .where(ProcessorIssue.buildingName == 'Edward Crown Center')\
    .group_by(StudentEmp.studentID)\
    .order_by(func.count(ProcessorIssue.caseNum).desc())
#print(stmt)
for student in session.execute(stmt):
    print(student)
