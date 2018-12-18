import sys

sys.path.append("..")

from models.performance import Performance

def test_sum():
    assert sum([1, 2, 3]) == 6, "Should be 6"

def test_of_performance_model():

    performance: Performance = Performance(

        defeated_by_gaps=1,
        defeated_by_opponent_type_1=2,
        defeated_by_opponent_type_2=3,
        defeated_by_opponent_type_3=4

    )

    df = performance.to_dataframe()

    print(df['defeated_by_gaps'])
    assert df['defeated_by_gaps'][0] == 1, "Should be 1"

if __name__ == "__main__":
    test_of_performance_model()
    test_sum()
    print("Everything passed")
