## Hint for cleaning up strings!

public class Strings {

    public static String removePunctuation(String s) {
        return s.replaceAll("\\p{Punct}", "");
    }

    public static String downCase(String s) {
        return s.toLowerCase();
    }

    public static void main(String[] argv) {
        String s1 = "Here, we have two(2) strings!  This is the f'irst.";
        String s2 = "& Another one just 4 fun";
        String s3 = "!@#$% )(**&";
		System.out.println(downCase(removePunctuation(s1)));
        System.out.println(downCase(removePunctuation(s2)));
        System.out.println(downCase(removePunctuation(s3)));
    }
}