import argparse
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from faker import Faker
import time
from datetime import datetime

# função para parsear a saída do parâmetro SILENT
def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

# Instancia a classe Faker
faker = Faker()

# Função MAIN
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate fake data...')

    parser.add_argument('--interval', type=float, default=0.5,
                        help='interval of generating fake data in seconds')
    parser.add_argument('-n', type=int, default=1,
                        help='sample size')
    parser.add_argument('--connection-string', '-cs', dest="connection_string", 
                        type=str, default='postgresql://postgres:Ney1987@localhost:5432/postgres',
                        help='Connection string to the database')
    parser.add_argument('--silent', type=str2bool, nargs='?',
                        const=True, default=False,
                        help="print fake data")

    args = parser.parse_args()

    print(f"Args parsed:")
    print(f"Interval: {args.interval}")
    print(f"Sample size: {args.n}")
    print(f"Connection string: {args.connection_string}", end='\n\n')

    #-----------------------------------------------------------------

    engine = create_engine(args.connection_string)

    print("Iniciando a simulacao...", end="\n\n")

    # Gera dados fake a faz ingestáo
    while True:
        rightnow = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        userid     = [np.random.randint(1, 31) for i in range(args.n)]
        productid  = [np.random.randint(1, 21) for i in range(args.n)]
        quantity   = [np.random.randint(1, 11) for i in range(args.n)]
        price      = [faker.pricetag() for i in range(args.n)]
        paymentmtd = [np.random.choice([1, 2], p=[0.5, 0.5]) for i in range(args.n)]
        paymentsts = [np.random.choice([1, 2, 3], p=[0.2, 0.1, 0.7]) for i in range(args.n)]
        dt_insert  = [rightnow for i in range(args.n)]
        dt_update  = [datetime.strptime(rightnow, "%Y-%m-%d %H:%M:%S.%f") for i in range(args.n)]

        df = pd.DataFrame({
            "userid": userid,
            "productid": productid,
            "quantity": quantity,
            "price": price,
            "paymentmtd": paymentmtd,
            "paymentsts": paymentsts,
            "dt_insert": dt_insert,
            "dt_update": dt_update
        })

        df.to_sql("sales", con=engine, if_exists="append", index=False, chunksize=args.n, method="multi")

        if not args.silent:
            print(df, end="\n\n")

        time.sleep(args.interval)