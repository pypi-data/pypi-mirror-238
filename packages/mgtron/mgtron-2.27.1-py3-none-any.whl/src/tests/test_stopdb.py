from src.db.models import save_to_database_for_stop
from src.db.models import get_sql_stop_info
from src.db.models import delete_sql_stop_info

def test_db_stop_value_1():
    save_to_database_for_stop("hooray")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "hooray"
    
def test_db_stop_value_2():
    delete_sql_stop_info()
    save_to_database_for_stop("good")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "good"
    
def test_db_stop_value_3():
    delete_sql_stop_info()
    save_to_database_for_stop("correct")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "correct"    
    
def test_db_stop_value_4():
    delete_sql_stop_info()
    save_to_database_for_stop("nice")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "nice"
    
def test_db_stop_value_5():
    delete_sql_stop_info()
    save_to_database_for_stop("great")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "great"

def test_db_stop_value_6():
    delete_sql_stop_info()
    save_to_database_for_stop("perfect")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "perfect"
    
def test_db_stop_value_7():
    delete_sql_stop_info()
    save_to_database_for_stop("awesome")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "awesome"
    
def test_db_stop_value_8():
    delete_sql_stop_info()
    save_to_database_for_stop("fantastic")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "fantastic"

def test_db_stop_value_9():
    delete_sql_stop_info()
    save_to_database_for_stop("amazing")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "amazing"
    
def test_db_stop_value_10():
    delete_sql_stop_info()
    save_to_database_for_stop("incredible")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "incredible"
    
def test_db_stop_value_11():
    delete_sql_stop_info()
    save_to_database_for_stop("wonderful")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "wonderful"
    
def test_db_stop_value_12():
    delete_sql_stop_info()
    save_to_database_for_stop("super")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "super"
    
def test_db_stop_value_13():
    delete_sql_stop_info()
    save_to_database_for_stop("excellent")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "excellent"

def test_db_stop_value_14():
    delete_sql_stop_info()
    save_to_database_for_stop("terrific")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "terrific"
    
def test_db_stop_value_15():
    delete_sql_stop_info()
    save_to_database_for_stop("outstanding")
    recieved_values = get_sql_stop_info()  
    for i in recieved_values:
        assert i[1] == "outstanding"
    
def test_db_stop_value_16():
    delete_sql_stop_info()
    save_to_database_for_stop("brilliant")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "brilliant"
    
def test_db_stop_value_17():
    delete_sql_stop_info()
    save_to_database_for_stop("genius")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "genius"
    
def test_db_stop_value_18():
    delete_sql_stop_info()
    save_to_database_for_stop("insurance")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "insurance"

def test_db_stop_value_19():
    delete_sql_stop_info()
    save_to_database_for_stop("wonder")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "wonder"
    
def test_db_stop_value_20():
    delete_sql_stop_info()
    save_to_database_for_stop("smoothing")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "smoothing"
    
def test_db_stop_value_21():
    delete_sql_stop_info()
    save_to_database_for_stop("addition")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "addition"
    
def test_db_stop_value_22():
    delete_sql_stop_info()
    save_to_database_for_stop("magnificent")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "magnificent"

def test_db_stop_value_23():
    delete_sql_stop_info()
    save_to_database_for_stop("magnificence")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "magnificence"
            
def test_db_stop_value_24():
    delete_sql_stop_info()
    save_to_database_for_stop("magnificently")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "magnificently"
    
def test_db_stop_value_25():
    delete_sql_stop_info()
    save_to_database_for_stop("magnifico")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "magnifico"
    
def test_db_stop_value_26():
    delete_sql_stop_info()
    save_to_database_for_stop("magnification")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "magnification"
    
def test_db_stop_value_27():
    delete_sql_stop_info()
    save_to_database_for_stop("subtraction")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "subtraction"

def test_db_stop_value_28():
    delete_sql_stop_info()
    save_to_database_for_stop("subtracted")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "subtracted"
    
def test_db_stop_value_29():
    delete_sql_stop_info()
    save_to_database_for_stop("subtracting")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "subtracting"
        
def test_db_stop_value_30():
    delete_sql_stop_info()
    save_to_database_for_stop("subtract")
    recieved_values = get_sql_stop_info()
    for i in recieved_values:
        assert i[1] == "subtract"

def test_db_stop_is_erased():
    delete_sql_stop_info()
    assert get_sql_stop_info() == []