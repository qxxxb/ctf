import components.naturalnumber.NaturalNumber;
import components.naturalnumber.NaturalNumber2;
import components.set.Set1L;
import components.stack.Stack2;

public final class SuperValidator {
    public static void testValidator1(String a, String b, String x) {
        // String as = Integer.toString(a);
        // String bs = Integer.toString(b);

        NaturalNumber an = new NaturalNumber2(a);
        NaturalNumber bn = new NaturalNumber2(b);

        System.out.println("a: " + an + ", b: " + b + ", x: " + x);
        NaturalNumber x_gen = Validator1Rev.secretOpDbg(an, bn);
        System.out.println("x (gen): " + x_gen);
        assert x.equals(x_gen.toString());

    }

    public static void testRevStack(String x, String b) {
        NaturalNumber xn = new NaturalNumber2(x);
        NaturalNumber bn = new NaturalNumber2(b);

        Stack2<NaturalNumber> s = Validator1Rev.revStack(xn);

        int padding_length = Validator1Rev.revSLength(xn, bn);
        Validator1Rev.pad(s, padding_length);

        System.out.println("s (rev): " + s);
    }

    public static void testRevLoopSingle() {
        {
            NaturalNumber a_rem2 = new NaturalNumber2(2);
            NaturalNumber b = new NaturalNumber2(1);
            NaturalNumber a_div = new NaturalNumber2(0);
            Set1L<NaturalNumber> as = Validator1Rev.revLoop(a_rem2, b, a_div);
            System.out.println("as: " + as);
        }
        {
            NaturalNumber a_rem2 = new NaturalNumber2(0);
            NaturalNumber b = new NaturalNumber2(4);
            NaturalNumber a_div = new NaturalNumber2(1);
            Set1L<NaturalNumber> as = Validator1Rev.revLoop(a_rem2, b, a_div);
            System.out.println("as: " + as);
        }
        {
            NaturalNumber a_rem2 = new NaturalNumber2(1);
            NaturalNumber b = new NaturalNumber2(14);
            NaturalNumber a_div = new NaturalNumber2(5);
            Set1L<NaturalNumber> as = Validator1Rev.revLoop(a_rem2, b, a_div);
            System.out.println("as: " + as);
        }
    }

    public static void testRevBsReliable(String b, String a) {
        NaturalNumber bn = new NaturalNumber2(b);
        NaturalNumber an = new NaturalNumber2(a);

        Stack2<NaturalNumber> bs = Validator1Rev.revBs(bn);

        int padding_length = Validator1Rev.revSLength(an, bn);
        Validator1Rev.pad(bs, padding_length);

        System.out.println("bs: " + bs);
    }

    public static void testRev(String x, String b) {
        NaturalNumber bn = new NaturalNumber2(b);
        NaturalNumber xn = new NaturalNumber2(x);

        Set1L<NaturalNumber> as = Validator1Rev.rev(xn, bn);
        for (NaturalNumber a : as) {
            System.out.println("a (gen): " + a);
        }
    }

    public static void testRevSLengthReliable(String a, String b) {
        NaturalNumber an = new NaturalNumber2(a);
        NaturalNumber bn = new NaturalNumber2(b);

        int s_length = Validator1Rev.revSLength(an, bn);
        System.out.println("s_length: " + s_length);
    }

    public static void testValidator1() {
        // String a = "53"; // 26 works too
        // String b = "17";
        // String x = "4";

        // String a = "3501";
        // String b = "3132";
        // String x = "6146";

        String a = "205";
        String b = "123";
        String x = "75";

        // String a = "199";
        // String b = "123";
        // String x = "78";

        // String a = "17";
        // String b = "14";
        // String x = "19";

        testValidator1(a, b, x);
        testRevSLengthReliable(a, b);
        testRevStack(x, b);
        // testRevLoopSingle();
        testRevBsReliable(b, a);
        testRev(x, b);
    }

    public static void crackValidator1() {
        String b = "7109340815511137277436103227634468226488145274050";
        String x = "135082787268816958421202995954498890820092905902643";

        testRev(x, b);

        // boolean result = Validator1.verify("7112389839740547540171064106410473651888145274050");
        // System.out.println("result: " + result);
    }

    public static void crackValidator2() throws Exception {
        Validator2.save();
        System.out.println(Validator2.verify("F3jk7h2"));
    }

    public static void dumpValidator1() {
        for (int a = 0; a < 16000; a++) {
            String b = "30";
            // String b = "7109340815511137277436103227634468226488145274050";
            // String x = "135082787268816958421202995954498890820092905902643";
            NaturalNumber an = new NaturalNumber2(a);
            NaturalNumber bn = new NaturalNumber2(b);
            NaturalNumber x = Validator1.secretOp(an, bn);
            System.out.println(a + ", " + b + ", " + x.toString());
        }
    }

    public static void main(String[] args) throws Exception {
        // testValidator1();
        crackValidator1();
        // dumpValidator1();
        // crackValidator2();
    }
}
