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
from sqlalchemy import distinct

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

    def __repr__(self) -> str:  # represents the object as a string
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

    departmentName: Mapped[str] = mapped_column(primary_key=True)

    managerID: Mapped[int] = mapped_column(ForeignKey("IT_manager.managerID"))
    manager: Mapped["Manager"] = relationship(back_populates="department")

    stuDepts: Mapped[List["StudentWorksIn"]] = relationship(back_populates="departmentRef",
                                                            cascade="all, delete-orphan")

    def __repr__(self) -> str:  # represents the object as a string
        return f"""Department(departmentName={self.departmentName!r}, managerID={self.managerID!r})"""


class StudentEmp(Base):
    __tablename__ = "studentEmp"

    studentID: Mapped[str] = mapped_column(primary_key=True)
    studentFName: Mapped[str] = mapped_column(String(50))
    studentLName: Mapped[str] = mapped_column(String(50))
    studentSalary: Mapped[int] = mapped_column()
    processorIssues: Mapped[List["ProcessorIssue"]] = relationship(back_populates="student",
                                                                   cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"studentID={self.studentID!r}, studentFName={self.studentFName!r}, studentLName={self.studentLName!r}," \
               f"studentSalary={self.studentSalary!r}"


class ProcessorIssue(Base):
    __tablename__ = "processorIssue"

    caseNum: Mapped[int] = mapped_column(primary_key=True)
    diagnosisDate: Mapped[str] = mapped_column(String(10))
    buildingName: Mapped[str] = mapped_column(String(50))
    partName: Mapped[str] = mapped_column(String(50))
    classNum: Mapped[int] = mapped_column()

    student_id: Mapped[str] = mapped_column(ForeignKey("studentEmp.studentID"))

    student: Mapped["StudentEmp"] = relationship(back_populates="processorIssues")

    def __repr__(self) -> str:  # represents the object as a string
        return f"ProcessorIssue(caseNum = {self.caseNum!r}, diagnosisDate = {self.diagnosisDate!r}," \
               f"buildingName = {self.buildingName!r}, partName = {self.partName!r})"


class Professor(Base):
    __tablename__ = "professor"

    professorID: Mapped[str] = mapped_column(primary_key=True)
    professorFName: Mapped[str] = mapped_column(String(50))
    professorLName: Mapped[str] = mapped_column(String(50))
    professorSalary: Mapped[int] = mapped_column()
    reports: Mapped[List["Report"]] = relationship(back_populates="professorRef", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Professor(professorID = {self.professorID!r}, professorFName = {self.professorFName!r}," \
               f"professorLName = {self.professorLName!r}, professorSalary = {self.professorSalary!r})"


class Report(Base):
    __tablename__ = "report"

    caseNum: Mapped[int] = mapped_column(ForeignKey("processorIssue.caseNum"), primary_key=True)
    professor_id: Mapped[str] = mapped_column(ForeignKey("professor.professorID"))
    professorRef: Mapped["Professor"] = relationship(back_populates="reports")

    def __repr__(self) -> str:
        return f"Report(caseNum = {self.caseNum!r})"


class StudentWorksIn(Base):
    __tablename__ = "studentWorksIn"

    studentID: Mapped[str] = mapped_column(ForeignKey("studentEmp.studentID"), primary_key=True)
    department_id: Mapped[str] = mapped_column(ForeignKey("IT_department.departmentName"))
    departmentRef: Mapped["Department"] = relationship(back_populates="stuDepts")

    def __repr__(self) -> str:
        return f"StudentWorksIn(StudentID={self.studentID!r})"


# Drop existing tables
Base.metadata.drop_all(engine)

# Create new tables with the updated schema
Base.metadata.create_all(engine)

# Insert Data
with Session(engine) as session:
    Marquinhos = Manager(
        managerID='00008554676',
        managerFName='Marquinhos',
        managerLName='Correa',
        managerSalary='155000',
        managedDName='Classroom Tech',
        specialists=[Specialist(specialistID='00001387051', specialistFName='Roberto', specialistLName='Carlos',
                                specialistSalary='43000'),
                     Specialist(specialistID='00002312829', specialistFName='Juan', specialistLName='Felix',
                                specialistSalary='83000'),
                     Specialist(specialistID='00006106639', specialistFName='Vinicius', specialistLName='Oliveira',
                                specialistSalary='48000'),
                     Specialist(specialistID='00008518764', specialistFName='Thiago', specialistLName='Silva',
                                specialistSalary='77000')],
    )
    Raphinha = Manager(
        managerID='00003489894',
        managerFName='Raphinha',
        managerLName='Belloli',
        managerSalary='77000',
        managedDName='Desktop Services',
        specialists=[Specialist(specialistID='00002130529', specialistFName='Richarlison', specialistLName='Andrade',
                                specialistSalary='43000'),
                     Specialist(specialistID='00006969520', specialistFName='Lucas', specialistLName='Paqueta',
                                specialistSalary='100000')],
    )

    Classroom_Tech = Department(departmentName='Classroom Tech', managerID='00008554676',
                                stuDepts=[StudentWorksIn(studentID='00007810224'),
                                          StudentWorksIn(studentID='00005637594'),
                                          StudentWorksIn(studentID='00002328669')]
                                )
    Desktop_Services = Department(departmentName='Desktop Services', managerID='00003489894',
                                  stuDepts=[StudentWorksIn(studentID='00007111521')])

    Cindy = StudentEmp(
        studentID='00007810224',
        studentFName='Cindy',
        studentLName='George',
        studentSalary='5000',
        # Cindy casNums = 1, 8, 9, 11
        processorIssues=[ProcessorIssue(caseNum='1', diagnosisDate='01/05/2023', buildingName='Cudahy Science Hall',
                                        partName='HDMI Couplers', classNum='108'),
                         ProcessorIssue(caseNum='8', diagnosisDate='03/19/2023', buildingName='Edward Crown Center',
                                        partName='Audio Extractor', classNum='210'),
                         ProcessorIssue(caseNum='9', diagnosisDate='03/22/2023', buildingName='Cudahy Science Hall',
                                        partName='HDMI Couplers', classNum='202'),
                         ProcessorIssue(caseNum='11', diagnosisDate='04/01/2023', buildingName='Edward Crown Center',
                                        partName='VGA Couplers', classNum='122')]
    )
    Barbara = StudentEmp(
        studentID='00005637594',
        studentFName='Barbara',
        studentLName='Wallace',
        studentSalary='5000',
        # Barbara casNums = 2, 7
        processorIssues=[ProcessorIssue(caseNum='2', diagnosisDate='01/09/2023', buildingName='Dumbach Hall',
                                        partName='Shure Microphone Transmitter', classNum='213'),
                         ProcessorIssue(caseNum='7', diagnosisDate='02/21/2023', buildingName='Edward Crown Center',
                                        partName='VGA Couplers', classNum='140')]
    )
    Roberto = StudentEmp(
        studentID='00002328669',
        studentFName='Roberto',
        studentLName='Firmino',
        studentSalary='5000',
        processorIssues=[ProcessorIssue(caseNum='3', diagnosisDate='01/09/2023', buildingName='Dumbach Hall',
                                        partName='Audio Extractor', classNum='303'),
                         ProcessorIssue(caseNum='5', diagnosisDate='01/15/2023', buildingName='Cueno Hall',
                                        partName='VGA Couplers', classNum='210'),
                         ProcessorIssue(caseNum='6', diagnosisDate='02/03/2023', buildingName='Information Commons',
                                        partName='Touch Panel', classNum='321')]
    )
    Harry = StudentEmp(
        studentID='00007111521',
        studentFName='Harry',
        studentLName='Maguire',
        studentSalary='2000',
        processorIssues=[ProcessorIssue(caseNum='4', diagnosisDate='01/10/2023', buildingName='Cueno Hall',
                                        partName='Touch Panel', classNum='100'),
                         ProcessorIssue(caseNum='10', diagnosisDate='03/22/2023', buildingName='Edward Crown Center',
                                        partName='Touch Panel', classNum='156'),
                         ProcessorIssue(caseNum='12', diagnosisDate='04/10/2023', buildingName='Information Commons',
                                        partName='Touch Panel', classNum='441')]
    )

    Devin = Professor(
        professorID='00005049786',
        professorFName='Devin',
        professorLName='Copeland',
        professorSalary='60000',
        reports=[Report(caseNum='1'), Report(caseNum='8')]
    )
    Francis = Professor(
        professorID='00001135183',
        professorFName='Francis',
        professorLName='Mendoza',
        professorSalary='88000',
        reports=[Report(caseNum='6'), Report(caseNum='9'), Report(caseNum='11')]
    )

    session.add_all([Marquinhos, Raphinha, Cindy, Barbara, Roberto, Classroom_Tech, Desktop_Services, Devin, Francis, Harry])
    session.commit()

session = Session(engine)

# specilistSalUnderManager    
specilistSalUnderManager = select(func.count(Specialist.specialistFName)).where(
    Specialist.managerID == Manager.managerID,
    Manager.managedDName == Department.departmentName,
    Manager.managerID == "00008554676",
    Department.departmentName == "Classroom Tech",
    Specialist.specialistSalary > 50000)

print("\n" + "### specilistSalUnderManager ###")
for Specialist in session.scalars(specilistSalUnderManager):
    print(str(Specialist))


# studentDiagnosesByPart
stmt = select(StudentEmp.studentFName, StudentEmp.studentLName, ProcessorIssue.partName, func.count(ProcessorIssue.caseNum))\
    .join(StudentEmp.processorIssues)\
    .join(Professor.reports)\
    .join(Department.stuDepts)\
    .where(Report.caseNum == ProcessorIssue.caseNum, Report.professor_id == '00001135183',
           StudentWorksIn.studentID == StudentEmp.studentID, StudentWorksIn.department_id == 'Classroom Tech')\
    .group_by(StudentEmp.studentID, ProcessorIssue.partName)\
    .order_by(func.count(ProcessorIssue.caseNum).desc(), StudentEmp.studentLName)

print("\n" + "### studentDiagnosesByPart ###")
for student in session.execute(stmt):
    print(student)