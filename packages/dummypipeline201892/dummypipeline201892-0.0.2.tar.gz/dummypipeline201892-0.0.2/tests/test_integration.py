from database import firebase
from firebase_admin import db, credentials

firebase.initialize_firebase()
def test_right_counter():
    # Inizializza il valore del contatore a un valore specifico (ad esempio, 5)
    username_counter = db.reference('users/utente_prova').child('counter').get()

    # Verifica se il valore del contatore è stato incrementato correttamente
    assert username_counter == 10


# Test per incremento
def test_increment_counter():
    # Inizializza il valore del contatore a un valore specifico (ad esempio, 5)
    username_ref = db.reference('users/damiano')
    username_ref.child('counter').set(5)

    # Verifica se la funzione restituisce True (operazione riuscita)
    assert firebase.increment_counter('damiano') == True

    # Verifica se il valore del contatore è stato incrementato correttamente
    assert username_ref.child('counter').get() == 6  # 5 (valore iniziale) + 1 = 6
