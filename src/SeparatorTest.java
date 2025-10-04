import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;
import java.util.List;

public class SeparatorTest {

    @Test
    void testMixedInput() {
        Separator.Result result = Separator.separateWordsAndDigits("apple,123,banana,456,cat,789");

        assertEquals(List.of("apple", "banana", "cat"), result.getWords());
        assertEquals(List.of("123", "456", "789"), result.getDigits());
    }

    @Test
    void testOnlyWords() {
        Separator.Result result = Separator.separateWordsAndDigits("dog,cat,fish");

        assertEquals(List.of("dog", "cat", "fish"), result.getWords());
        assertTrue(result.getDigits().isEmpty());
    }

    @Test
    void testOnlyDigits() {
        Separator.Result result = Separator.separateWordsAndDigits("1,2,3,4");

        assertTrue(result.getWords().isEmpty());
        assertEquals(List.of("1", "2", "3", "4"), result.getDigits());
    }

    @Test
    void testEmptyInput() {
        Separator.Result result = Separator.separateWordsAndDigits("");
        assertTrue(result.getWords().isEmpty());
        assertTrue(result.getDigits().isEmpty());
    }

    @Test
    void testNullInput() {
        Separator.Result result = Separator.separateWordsAndDigits(null);
        assertTrue(result.getWords().isEmpty());
        assertTrue(result.getDigits().isEmpty());
    }

    @Test
    void testWithSpaces() {
        Separator.Result result = Separator.separateWordsAndDigits(" apple , 123 , banana , 456 ");

        assertEquals(List.of("apple", "banana"), result.getWords());
        assertEquals(List.of("123", "456"), result.getDigits());
    }
}
