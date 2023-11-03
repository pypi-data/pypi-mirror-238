"""
Test case for PITag.
.. since: 0.2
"""

# -*- coding: utf-8 -*-
# Copyright (c) 2022 Endeavour Mining
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to read
# the Software only. Permissions is hereby NOT GRANTED to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from sqlalchemy.engine import Connection, Engine  # type: ignore
from sqlalchemy import text  # type: ignore
from testcontainers.postgres import PostgresContainer  # type: ignore
from edv_dwh_connector.dwh import Dwh
from edv_dwh_connector.pg_dwh import PgDwh


class AdaptedPostreSQL(PostgresContainer):
    """
    Adapted PostgreSQL container to fix host.
    .. since: 0.2
    """

    def __init__(self) -> None:
        """
        Ctor.
        """
        super().__init__('postgres:14.5')

    def get_connection_url(self, host: str = None):
        """
        Connection url.
        :param host: Hostname
        :return: Url
        """
        return super().get_connection_url(host) \
            .replace('localnpipe', 'localhost')


# flake8: noqa
SCHEMA = """
    CREATE TABLE IF NOT EXISTS Dim_PI_tag (
        tag_PK SERIAL,
        code CHARACTER VARYING (25) NOT NULL,
        name CHARACTER VARYING (225) NOT NULL,
        web_id CHARACTER VARYING (225) NOT NULL,
        uom CHARACTER VARYING (10),
        CONSTRAINT uq_dim_pi_tag_code UNIQUE (code),
        CONSTRAINT pk_dim_tag PRIMARY KEY (tag_PK)
    );
    CREATE TABLE IF NOT EXISTS Dim_Time(
        time_PK INTEGER NOT NULL,
        time_value CHARACTER(8) NOT NULL,
        hours_24 INTEGER NOT NULL,
        hours_12 INTEGER NOT NULL,
        hour_minutes INTEGER  NOT NULL,
        minutes_second INTEGER  NOT NULL,
        day_minutes INTEGER NOT NULL,
        hour_second INTEGER NOT NULL,
        day_second INTEGER NOT NULL,
        day_time_name CHARACTER VARYING (20) NOT NULL,
        day_night CHARACTER VARYING (20) NOT NULL,
        CONSTRAINT pk_dim_time PRIMARY KEY (time_PK)
    );
    CREATE TABLE IF NOT EXISTS Dim_Date(
        date_PK NUMERIC NOT NULL,
        date_value date NOT NULL,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL,
        monthname CHARACTER (12)  NOT NULL,
        day INTEGER NOT NULL,
        dayofyear INTEGER NOT NULL,
        weekdayname CHARACTER (12) NOT NULL,
        calendarweek INTEGER NOT NULL,
        formatteddate CHARACTER (10) NOT NULL,
        quartal CHARACTER (2) NOT NULL,
        yearquartal CHARACTER (7) NOT NULL,
        yearmonth CHARACTER (7) NOT NULL,
        yearcalendarweek CHARACTER (7) NOT NULL,
        weekend CHARACTER (10) NOT NULL,
        cwstart date NOT NULL,
        cwend date NOT NULL,
        monthstart date NOT NULL,
        monthend date NOT NULL,
        CONSTRAINT pk_dim_date PRIMARY KEY (date_PK)
    );
    CREATE TABLE IF NOT EXISTS Fact_PI_measure (
        tag_PK INTEGER NOT NULL,
        date_PK INTEGER NOT NULL,
        time_PK INTEGER NOT NULL,
        millisecond NUMERIC DEFAULT 0 NOT NULL,
        value NUMERIC(8,3) NOT NULL,
        CONSTRAINT fk_pi_measure_dim_pitag FOREIGN KEY (tag_PK) REFERENCES dim_pi_tag (tag_PK) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_fact_pi_measure_dim_date FOREIGN KEY (date_PK) REFERENCES dim_date (date_PK) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_fact_pi_measure_dim_time FOREIGN KEY (time_PK) REFERENCES dim_time (time_PK) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT pk_fact_pi_measure PRIMARY KEY (date_PK, time_PK, tag_PK,millisecond)
    );
    CREATE TABLE IF NOT EXISTS Fact_PI_measure_Hist (
        tag_PK INTEGER NOT NULL,
        date_PK INTEGER NOT NULL,
        time_PK INTEGER NOT NULL,
        millisecond NUMERIC DEFAULT 0 NOT NULL,
        value NUMERIC(8,3) NOT NULL,
        CONSTRAINT fk_pi_measure_hist_dim_pitag FOREIGN KEY (tag_PK) REFERENCES dim_pi_tag (tag_PK) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_fact_pi_measure_hist_dim_date FOREIGN KEY (date_PK) REFERENCES dim_date (date_PK) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_fact_pi_measure_hist_dim_time FOREIGN KEY (time_PK) REFERENCES dim_time (time_PK) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT pk_fact_pi_measure_hist PRIMARY KEY (date_PK, time_PK, tag_PK,millisecond)
    );
    CREATE  VIEW v_pi_measure_all AS
            SELECT CAST(dd.date_value AS TEXT)||' '||dt.time_value||'.'||LPAD(fp.millisecond::text, 3, '0') full_datetime, dtg.code, dtg.name, dtg.uom, fp.value
        FROM dim_date dd,dim_time dt,dim_pi_tag dtg,fact_pi_measure fp
        WHERE fp.date_pk = dd.date_pk
        AND fp.time_pk = dt.time_pk
        AND fp.tag_pk = dtg.tag_pk;
    INSERT INTO  Dim_Time
    SELECT  CAST(TO_CHAR(second, 'hh24miss') AS numeric) time_PK,
        TO_CHAR(second, 'hh24:mi:ss') AS time_value,
        -- Hour of the day (0 - 23)
        EXTRACT (hour FROM  second) AS hour_24,
        -- Hour of the day (0 - 11)
        TO_NUMBER(TO_CHAR(second, 'hh12'),'99') hour_12,
        -- Hour minute (0 - 59)
        EXTRACT(minute FROM second) hour_minutes,
        -- minute second (0 - 59)
        EXTRACT(second FROM second) minutes_second,
        -- Minute of the day (0 - 1439)
        EXTRACT(hour FROM second)*60 + EXTRACT(minute FROM second) day_minutes,
        -- second of the hour (0 - 3599)
        EXTRACT(minute FROM second)*60 + EXTRACT(second FROM second) hour_second,
        -- second of the day (0 - 86399)
        EXTRACT(hour FROM second)*3600 + EXTRACT(minute FROM second)*60 + EXTRACT(second FROM second) day_second,
        -- Names of day periods
        CASE WHEN TO_CHAR(second, 'hh24:mi') BETWEEN '06:00' AND '08:29'
        THEN 'Morning'
        WHEN TO_CHAR(second, 'hh24:mi') BETWEEN '08:30' AND '11:59'
        THEN 'AM'
        WHEN TO_CHAR(second, 'hh24:mi') BETWEEN '12:00' AND '17:59'
        THEN 'PM'
        WHEN TO_CHAR(second, 'hh24:mi') BETWEEN '18:00' AND '22:29'
        THEN 'Evening'
        ELSE 'Night'
        END AS day_time_name,
        -- Indicator of day or night
        CASE WHEN TO_CHAR(second, 'hh24:mi') BETWEEN '07:00' AND '19:59' THEN 'Day'
        ELSE 'Night'
        END AS day_night
    FROM (SELECT '0:00:00'::time + (sequence.second || ' seconds')::interval AS second
        FROM generate_series(0,86399) AS sequence(second)
        GROUP BY sequence.second
        ) DQ
    ORDER BY 1;
    INSERT INTO  Dim_Date
    SELECT
        CAST(TO_CHAR(datum, 'yyyymmdd') as numeric) date_PK,
        datum as Date,
        EXTRACT(year FROM datum) AS Year,
        EXTRACT(month FROM datum) AS Month,
        -- Localized month name
        TO_CHAR(datum, 'TMMonth') AS MonthName,
        EXTRACT(day FROM datum) AS Day,
        EXTRACT(doy FROM datum) AS DayOfYear,
        -- Localized weekday
        TO_CHAR(datum, 'TMDay') AS WeekdayName,
        -- ISO calendar week
        EXTRACT(week FROM datum) AS CalendarWeek,
        TO_CHAR(datum, 'dd-mm-yyyy') AS FormattedDate,
        'Q' || TO_CHAR(datum, 'Q') AS Quartal,
        TO_CHAR(datum, 'yyyy/"Q"Q') AS YearQuartal,
        TO_CHAR(datum, 'yyyy/mm') AS YearMonth,
        -- ISO calendar year and week
        TO_CHAR(datum, 'iyyy/IW') AS YearCalendarWeek,
        -- Weekend
        CASE WHEN EXTRACT(isodow FROM datum) in (6, 7) THEN 'Weekend' ELSE 'Weekday' END AS Weekend,
        -- ISO start and end of the week of this date
        datum + (1 - EXTRACT(isodow FROM datum))::integer AS CWStart,
        datum + (7 - EXTRACT(isodow FROM datum))::integer AS CWEnd,
        -- Start and end of the month of this date
        datum + (1 - EXTRACT(day FROM datum))::integer AS MonthStart,
        (datum + (1 - EXTRACT(day FROM datum))::integer + '1 month'::interval)::date - '1 day'::interval AS MonthEnd
    FROM (
        -- There are 1 leap year in this range, so calculate 365 records
        SELECT '2022-01-01'::DATE + sequence.day AS datum
        FROM generate_series(0,365) AS sequence(day)
        GROUP BY sequence.day
         ) DQ
    ORDER BY 1;
    INSERT INTO Dim_PI_Tag (code, name, uom, web_id)
    VALUES
        ('AI162003_SCLD', 'Carbon Scout Tank 1 Carbon Concentration Scaled Value', 'g/l', 'F1DPmN2MpX8PREOtdbEZ56sypATAIAAASVRZLVNSVi1QSS1ISTAxXEFJMTYyMDAzX1NDTEQ'),
        ('AI162007_SCLD', 'Carbon Scout Tank 3 pH Scaled Value', 'pH', 'F1DPmN2MpX8PREOtdbEZ56sypAUAIAAASVRZLVNSVi1QSS1ISTAxXEFJMTYyMDA3X1NDTEQ'),
        ('AI162014_SCLD', 'Carbon Scout Tank 5 DO Scaled Value', 'ppm', 'F1DPmN2MpX8PREOtdbEZ56sypAVwIAAASVRZLVNSVi1QSS1ISTAxXEFJMTYyMDE0X1NDTEQ');
    CREATE TABLE IF NOT EXISTS Dim_Material (
        material_PK SERIAL,
        name CHARACTER VARYING(25) NOT NULL,
        description CHARACTER VARYING(225) NULL,
        CONSTRAINT pk_dim_material PRIMARY KEY (material_PK)
    
    );
    CREATE TABLE IF NOT EXISTS Dim_Material_charac (
        materialcharac_PK SERIAL,
        name CHARACTER VARYING(225) NOT NULL,
        uom CHARACTER VARYING(5) NULL,
        CONSTRAINT pk_dim_materialcharac PRIMARY KEY (materialcharac_PK)
    
    );
    CREATE TABLE IF NOT EXISTS Dim_Blend_charac (
        Blendcharac_PK SERIAL,
        name CHARACTER VARYING(225) NOT NULL,
        uom CHARACTER VARYING (5) NULL,
        CONSTRAINT pk_dim_Blendcharac PRIMARY KEY (Blendcharac_PK)
    );
    CREATE TABLE IF NOT EXISTS Dim_Sequence (
        sequence_PK SERIAL,
        name CHARACTER VARYING(10) NOT NULL,
        CONSTRAINT pk_dim_sequence PRIMARY KEY (sequence_PK)
    );
    CREATE TABLE IF NOT EXISTS Dim_Pit (
        pit_PK SERIAL,
        name CHARACTER VARYING(225) NOT NULL,
        abbreviation CHARACTER VARYING(225) NULL,
        CONSTRAINT pk_dim_pit PRIMARY KEY (pit_PK)
    );
    CREATE TABLE IF NOT EXISTS Fact_Material_measure (
        date_PK INTEGER NOT NULL,
        sequence_PK INTEGER NOT NULL,
        materialcharac_PK INTEGER NOT NULL,
        pit_PK INTEGER NOT NULL,
        material_PK INTEGER NOT NULL,
        value NUMERIC(8,3) NOT NULL,
        CONSTRAINT fk_fact_mat_measure_dim_date  FOREIGN KEY (Date_PK) REFERENCES Dim_Date (Date_PK) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_fact_mat_measure_dim_sequence  FOREIGN KEY (sequence_PK) REFERENCES Dim_Sequence (sequence_PK)ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_fact_mat_measure_dim_pit FOREIGN KEY (pit_PK) REFERENCES Dim_Pit (pit_PK)ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_fact_mat_measure_dim_material FOREIGN KEY (material_PK) REFERENCES Dim_Material (material_PK) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_fact_mat_measure_dim_mat_charac FOREIGN KEY (materialcharac_PK) REFERENCES Dim_Material_charac (materialcharac_PK)ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT pk_fact_mat_measure PRIMARY KEY (date_PK, sequence_PK, materialcharac_PK,pit_PK,material_PK) 
    );
    CREATE TABLE IF NOT EXISTS Fact_Blend_Sequence (
        Date_PK INTEGER NOT NULL,
        sequence_PK INTEGER NOT NULL,
        name CHARACTER VARYING(225) NULL,
        CONSTRAINT fk_fact_blend_sequence_dim_date FOREIGN KEY (Date_PK) REFERENCES Dim_Date (Date_PK) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_fact_blend_sequence_dim_sequence  FOREIGN KEY (sequence_PK) REFERENCES Dim_Sequence (sequence_PK)ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT pk_fact_blend_sequence PRIMARY KEY (date_PK, sequence_PK) 	
    );
    CREATE TABLE IF NOT EXISTS Fact_Blend_Measure (
        Date_PK INTEGER NOT NULL,
        sequence_PK INTEGER NOT NULL,
        blendcharac_PK INTEGER NOT NULL,
        value NUMERIC(8,3) NOT NULL,
        CONSTRAINT fk_fact_blend_measure_dim_date  FOREIGN KEY (Date_PK) REFERENCES Dim_Date (Date_PK) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_fact_blend_measure_dim_sequence  FOREIGN KEY (sequence_PK) REFERENCES Dim_Sequence (sequence_PK) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT fk_fact_blend_measure_dim_blendcharac FOREIGN KEY (blendcharac_PK) REFERENCES Dim_Blend_charac (blendcharac_PK) ON DELETE RESTRICT ON UPDATE CASCADE,
        CONSTRAINT pk_fact_blend_measure PRIMARY KEY (date_PK, sequence_PK,blendcharac_PK) 
    );
    CREATE OR REPLACE FUNCTION get_type_machine(material character varying)  
    RETURNS character varying  
    LANGUAGE plpgsql  
    AS  
    $$  
    DECLARE  
     machine character varying;  
    BEGIN  
       SELECT (CASE WHEN UPPER (LEFT('material',3)) = 'SUR' 
             OR UPPER (LEFT('material',3)) = 'COS' 
        THEN 'SURGE BIN'
        ELSE 'CRUSHER'
        END)   
       INTO machine; 
       RETURN machine;  
    END;  
    $$; 
    CREATE  VIEW v_blend_proposal AS
        SELECT dd.date_value full_date, count(*) nb_sequence
        FROM dim_date dd,fact_blend_sequence fbs
        WHERE fbs.date_pk = dd.date_pk
        GROUP BY 1;
    CREATE  VIEW v_blend_measure AS
        SELECT dd.date_value full_date, ds.name seq_name , dbc.name bend_char_name, dbc.uom , fbm.value
        FROM dim_date dd,dim_blend_charac dbc, dim_sequence ds, fact_blend_measure fbm
        WHERE fbm.date_pk = dd.date_pk
        AND fbm.sequence_pk = ds.sequence_pk
        AND fbm.blendcharac_pk = dbc.blendcharac_pk;  
    CREATE  VIEW  v_material_measure AS
        SELECT dd.date_value full_date, ds.name seq_name , dp.name pit_name ,dm.name mat_name, get_type_machine(dm.name) machine, dmc.name chara_name,dmc.uom , fmm.value
        FROM dim_date dd,dim_material_charac dmc, dim_pit dp, dim_sequence ds, dim_material dm, fact_material_measure fmm
        WHERE fmm.date_pk = dd.date_pk
        AND fmm.sequence_pk = ds.sequence_pk
        AND fmm.materialcharac_pk = dmc.materialcharac_pk
        AND fmm.pit_pk = dp.pit_pk
        AND fmm.material_pk = dm.material_pk;
    CREATE OR REPLACE FUNCTION timestamp_to_seconds(timestamp_t  TIMESTAMP WITH TIME ZONE)
    RETURNS DOUBLE PRECISION AS $$
        SELECT EXTRACT(epoch from timestamp_t)
    $$ LANGUAGE SQL;
    CREATE OR REPLACE FUNCTION linear_interpolate(x_i DOUBLE PRECISION, 
        x_0 DOUBLE PRECISION, 
        y_0 numeric(8, 3), 
        x_1 DOUBLE PRECISION, 
        y_1 numeric(8, 3))
    RETURNS numeric(8, 3) AS $$
        SELECT (($5 - $3) / ($4 - $2)) * ($1 - $2) + $3;
    $$ LANGUAGE SQL;
    CREATE OR REPLACE FUNCTION linear_interpolate(x_i TIMESTAMP WITH TIME ZONE, x_0 TIMESTAMP WITH TIME ZONE, y_0 numeric(8, 3), x_1 TIMESTAMP WITH TIME ZONE, y_1 numeric(8, 3))
    RETURNS DOUBLE PRECISION AS $$
        SELECT linear_interpolate(
            timestamp_to_seconds($1), 
            timestamp_to_seconds($2), 
            $3, 
            timestamp_to_seconds($4),
            $5
        );
    $$ LANGUAGE SQL;
    INSERT INTO dim_sequence (name)
    VALUES
        ('Sequence 1'),
        ('Sequence 2'),
        ('Sequence 3'),
        ('Sequence 4'),
        ('Sequence 5'),
        ('Sequence 6'),
        ('Sequence 7'),
        ('Sequence 8'),
        ('Sequence 9');
    INSERT INTO dim_material_charac (name, uom)
    VALUES
        ('Au grade', 'g/t'),
        ('Soluble copper', 'ppm'),
        ('As', 'ppm'),
        ('Moisture', 'per'),
        ('Indicative Rec', 'per'),
        ('Bucket', 'N/D'),
        ('Available Tons', 'N/D'),
        ('Prop', 'per');
    INSERT INTO dim_blend_charac (name, uom)
    VALUES
        ('Average Au Grade', 'g/t'),
        ('Soluble Copper', 'ppm'),
        ('Arsenic', 'ppm'),
        ('Moisture Estimated', 'per'),
        ('Percentage of Oxide/Transition', 'per'),
        ('Percentage of Fresh', 'per'),
        ('Estimated Recovery Blend', 'per');
    INSERT INTO dim_material (name)
    VALUES
        ('VSM_LG_HG_AS'),
        ('LG_HG_OX_TR_HCU'),
        ('LEP_HG_FR_LCU'),
        ('SURGE_BIN_OX_LG_HG'),
        ('SURGE_BIN_FR_LG_HG');
    INSERT INTO dim_pit (name, abbreviation)
    VALUES
        ('DAAPLEU', 'DAA'),
        ('WAL/BAK', 'WAL'),
        ('LEP', 'LEP'),
        ('LEP/WAL/BAK', 'LEP'),
        ('DAA/LEP', 'DAA');
    INSERT INTO fact_blend_sequence (date_pk, sequence_pk, name)
    VALUES
        (20221007, 1, 'WHEN THE CRUSHER COME ON LINE'),
        (20221007, 2, 'IF LEP_HG_FR_LCU  IS  FINISHED'),
        (20221007, 3, 'DURING  THE MILL  SHUTDOWN');
    INSERT INTO fact_blend_measure (date_pk, sequence_pk, blendcharac_pk, value)
    VALUES
        (20221007, 1, 1, 2.26778845393768),
        (20221007, 1, 2, 465.393774803503),
        (20221007, 1, 3, 527.253135896732),
        (20221007, 1, 4, 0.171793423848946),
        (20221007, 1, 5, 0.475482487210508),
        (20221007, 1, 6, 0.524517512789492),
        (20221007, 1, 7, 0.838078468633372),
        (20221007, 2, 1, 2.14555125393768),
        (20221007, 2, 2, 523.878966653503),
        (20221007, 2, 3, 775.647317346731),
        (20221007, 2, 4, 0.171793423848946),
        (20221007, 2, 5, 0.575482487210508),
        (20221007, 2, 6, 0.424517512789492),
        (20221007, 2, 7, 0.769937861799003),
        (20221007, 3, 1, 3.47),
        (20221007, 3, 2, 15),
        (20221007, 3, 3, 2576.963614),
        (20221007, 3, 4, 0.21),
        (20221007, 3, 5, 0),
        (20221007, 3, 6, 1),
        (20221007, 3, 7, 0.5925);
    INSERT INTO fact_material_measure (date_pk, sequence_pk, pit_pk, materialcharac_pk, material_pk, value)
    VALUES
        (20221007, 1, 1, 1, 1, 3.470744),
        (20221007, 1, 1, 2, 1, 15),
        (20221007, 1, 1, 3, 1, 2576.963614),
        (20221007, 1, 1, 4, 1, 0.12),
        (20221007, 1, 1, 5, 1, 0.5925),
        (20221007, 1, 1, 6, 1, 1.16831896551724),
        (20221007, 1, 1, 7, 1, 9825.01050778523),
        (20221007, 1, 1, 8, 1, 0.1),
        (20221007, 1, 2, 1, 2, 2.034366),
        (20221007, 1, 2, 2, 2, 1114.727882),
        (20221007, 1, 2, 3, 2, 92.965011),
        (20221007, 1, 2, 4, 2, 0.12),
        (20221007, 1, 2, 5, 2, 0.927584),
        (20221007, 1, 2, 6, 2, 1.46513513513513),
        (20221007, 1, 2, 7, 2, 2226.18968148191),
        (20221007, 1, 2, 8, 2, 0.1),
        (20221007, 1, 3, 1, 3, 3.07),
        (20221007, 1, 3, 2, 3, 79),
        (20221007, 1, 3, 3, 3, 93),
        (20221007, 1, 3, 4, 3, 0.21),
        (20221007, 1, 3, 5, 3, 0.921809),
        (20221007, 1, 3, 6, 3, 2.33663793103448),
        (20221007, 1, 3, 7, 3, 2007.11742452772),
        (20221007, 1, 3, 8, 3, 0.2),
        (20221007, 1, 4, 1, 4, 2.425),
        (20221007, 1, 4, 2, 4, 947),
        (20221007, 1, 4, 3, 4, 92.991842),
        (20221007, 1, 4, 4, 4, 0.21),
        (20221007, 1, 4, 5, 4, 0.892351),
        (20221007, 1, 4, 6, 4, 3),
        (20221007, 1, 4, 7, 4, 5380.98),
        (20221007, 1, 4, 8, 4, 0.275482487210508),
        (20221007, 1, 5, 1, 5, 1.555746),
        (20221007, 1, 5, 2, 5, 185.470947),
        (20221007, 1, 5, 3, 5, 920.834673),
        (20221007, 1, 5, 4, 5, 0.12),
        (20221007, 1, 5, 5, 5, 0.781386),
        (20221007, 1, 5, 6, 5, 1),
        (20221007, 1, 5, 7, 5, 5450),
        (20221007, 1, 5, 8, 5, 0.224517512789492);
    """


# pylint: disable=too-few-public-methods
class PgDwhForTests(Dwh):
    """PostgreSQL data warehouse for tests"""

    def __init__(self, engine: Engine):
        self.__dwh = PgDwh(engine)
        with self.__dwh.connection() as conn:
            conn.execute(
                text(SCHEMA)
            )

    def begin(self) -> Connection:
        return self.__dwh.begin()

    def terminate(self) -> None:
        self.__dwh.terminate()

    def connection(self) -> Connection:
        return self.__dwh.connection()

    def engine(self) -> Engine:
        return self.__dwh.engine()
