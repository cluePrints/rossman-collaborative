# -*- coding: utf-8 -*-
import click
import logging
import pandas as pd
from pathlib import Path
from dotenv import find_dotenv, load_dotenv


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    normalize_google_trends(input_filepath, output_filepath)


def normalize_google_trends(raw_data, normalized_data):
    trends = pd.read_csv(f'{raw_data}/googletrend.csv')
    trends['State'] = trends['file'].str.split('_', expand=True)[2]

    # HB, NI used with the rest of the data
    trends.loc[trends['State'] =='NI', 'State']='HB,NI'

    # let's stick to CamelCase for original fields and add _mod for types and calcs
    trends.columns = ['File', 'Week', 'Trend', 'State']

    trends['WeekStart_Sun'] = pd.to_datetime(trends['Week'].str.split(' - ', expand=True)[0])
    trends['WeekStart'] = trends['WeekStart_Sun'] - pd.to_timedelta(arg=trends['WeekStart_Sun'].dt.weekday, unit='D')
    trends.drop(['File', 'Week', 'WeekStart_Sun'], axis=1, inplace=True)

    trends.to_csv(f'{normalized_data}/googletrend.csv', index=False) 


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
