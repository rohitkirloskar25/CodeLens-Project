import java.util.ArrayList;
import java.util.List;

public class Separator {
    public static class Result {
        private final List<String> words;
        private final List<String> digits;

        public Result(List<String> words, List<String> digits) {
            this.words = words;
            this.digits = digits;
        }

        public List<String> getWords() {
            return words;
        }

        public List<String> getDigits() {
            return digits;
        }
    }

    public static Result separateWordsAndDigits(String input) {
        if (input == null || input.isEmpty()) {
            return new Result(new ArrayList<>(), new ArrayList<>());
        }

        String[] parts = input.split(",");
        List<String> words = new ArrayList<>();
        List<String> digits = new ArrayList<>();

        for (String part : parts) {
            String trimmed = part.trim();
            if (trimmed.matches("\\d+")) {
                digits.add(trimmed);
            } else {
                words.add(trimmed);
            }
        }

        return new Result(words, digits);
    }

    public static void main(String[] args) {
        String input = "apple,123,banana,456,cat,789";
        Result result = separateWordsAndDigits(input);

        System.out.println("Words: " + result.getWords());
        System.out.println("Digits: " + result.getDigits());
    }
}
