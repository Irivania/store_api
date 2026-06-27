import asyncio
from store.db.mongo import db_client

async def main():
    try:
        # Pega o cliente a partir do seu objeto db_client
        client = db_client.get()
        
        # O Motor usa a sintaxe 'command' diretamente no cliente
        await client.admin.command('ping')
        
        print("CONEXÃO COM ATLAS: SUCESSO!")
    except Exception as e:
        print(f"ERRO NA CONEXÃO: {e}")
        # Exibe o tipo de erro para ajudar no diagnóstico
        print(f"Tipo do erro: {type(e)}")

if __name__ == "__main__":
    asyncio.run(main())