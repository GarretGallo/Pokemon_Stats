from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, DECIMAL, text
from sqlalchemy.orm import declarative_base

from PokemonStats_Transform import tournaments, usage_items, usage_mons, usage_moves, usage_tera

Base = declarative_base()

#---Database Credentials---#
USERNAME = '***'
PASSWORD = '***'
HOST = '***'
DATABASE = '***'

engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}")

#---Create SQL Tables---#
class Tournaments(Base):
    __tablename__ = 'tournament_directory'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    tournament = Column(String(200), nullable=False)
    start_date = Column(Date, nullable=False)
    regulation = Column(String(200), nullable=False)
    event_level = Column(String(200), nullable=False)

class PokemonUsage(Base):
    __tablename__ = 'pokemon_usage_stats'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    tournament = Column(String(200))
    pokemon = Column(String(200), nullable=False)
    teams_used = Column(Integer, nullable=False)
    usage_perc = Column(DECIMAL(10,2), nullable=False)
    rank = Column(Integer, nullable=False)

class ItemUsage(Base):
    __tablename__ = 'item_usage_stats'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    tournament = Column(String(200))
    pokemon = Column(String(200), nullable=False)
    item = Column(String(200), nullable=False)
    item_count = Column(Integer, nullable=False)
    usage_perc = Column(DECIMAL(10,2), nullable=False)

class MoveUsage(Base):
    __tablename__ = 'move_usage_stats'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    tournament = Column(String(200))
    pokemon = Column(String(200), nullable=False)
    move = Column(String(200), nullable=False)
    move_count = Column(Integer, nullable=False)
    usage_perc = Column(DECIMAL(10,2), nullable=False)

class TeraUsage(Base):
    __tablename__ = 'tera_usage_stats'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    tournament = Column(String(200))
    pokemon = Column(String(200), nullable=False)
    tera_type = Column(String(200), nullable=False)
    teams_used = Column(Integer, nullable=False)
    usage_perc = Column(DECIMAL(10,2), nullable=False)

#---Upload Data---#
Base.metadata.create_all(engine)

tournaments.to_sql('tournament_directory', con=engine, index=False, if_exists='replace')
usage_mons.to_sql('pokemon_usage_stats', con=engine, index=False, if_exists='replace')
usage_items.to_sql('item_usage_stats', con=engine, index=False, if_exists='replace')
usage_moves.to_sql('move_usage_stats', con=engine, index=False, if_exists='replace')
usage_tera.to_sql('tera_usage_stats', con=engine, index=False, if_exists='replace')
