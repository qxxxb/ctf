import components.naturalnumber.NaturalNumber;
import components.naturalnumber.NaturalNumber2;
import components.set.Set1L;
import components.stack.Stack2;

public class Validator1Rev {
    static boolean verify(String s) {
        if (s.charAt(0) == '0') {
            return false;
        } else {
            NaturalNumber a = new NaturalNumber2(s);
            NaturalNumber b = new NaturalNumber2("17");

            NaturalNumber combo = secretOp(a, b);
            System.out.println("Combo: " + combo);

            NaturalNumber expected = new NaturalNumber2("30");
            System.out.println("Expected: " + expected);

            return combo.equals(expected);
        }
    }

    static NaturalNumber secretOp(NaturalNumber a, NaturalNumber b) {
        NaturalNumber three = a.newInstance();
        NaturalNumber two = a.newInstance();
        two.setFromInt(2);
        three.setFromInt(3);
        Stack2<NaturalNumber> s = new Stack2<NaturalNumber>();

        NaturalNumber z1;
        while (!a.isZero() || !b.isZero()) {
            z1 = a.divide(three);
            NaturalNumber z2 = b.divide(three).divide(two);
            if (z2.isZero()) {
                z1.add(two);
            } else {
                z1.increment();
            }

            z1 = z1.divide(three);
            s.push(z1);
        }

        System.out.println("s: " + s);

        z1 = a.newInstance();

        while (s.length() > 0) {
            z1.multiply(three);
            z1.add(s.pop());
        }

        return z1;
    }

    static NaturalNumber secretOpDbg(NaturalNumber a, NaturalNumber b) {
        NaturalNumber three = a.newInstance();
        NaturalNumber two = a.newInstance();
        two.setFromInt(2);
        three.setFromInt(3);
        Stack2<NaturalNumber> s = new Stack2<NaturalNumber>();
        Stack2<String> as = new Stack2<String>();
        Stack2<String> bs = new Stack2<String>();

        NaturalNumber z1;
        while (!a.isZero() || !b.isZero()) {
            as.push(a.toString());
            bs.push(b.toString());

            z1 = a.divide(three);
            NaturalNumber z2 = b.divide(three).divide(two);
            if (z2.isZero()) {
                z1.add(two);
            } else {
                z1.increment();
            }

            z1 = z1.divide(three);
            s.push(z1);
        }

        System.out.println("as: " + as);
        System.out.println("bs: " + bs);
        System.out.println("s: " + s);

        z1 = a.newInstance();

        while (s.length() > 0) {
            z1.multiply(three);
            z1.add(s.pop());
        }

        return z1;
    }

    // Side-effectless math

    static NaturalNumber divideN(NaturalNumber a, NaturalNumber b) {
        // clone a
        NaturalNumber a1 = a.newInstance();
        a1.copyFrom(a);

        a1.divide(b);
        return a1;
    }

    static NaturalNumber remainderN(NaturalNumber x, NaturalNumber base) {
        // Clone x
        NaturalNumber x1 = x.newInstance();
        x1.copyFrom(x);

        return x1.divide(base);
    }

    static NaturalNumber multiplyN(NaturalNumber a, NaturalNumber b) {
        // Clone a
        NaturalNumber a1 = a.newInstance();
        a1.copyFrom(a);

        a1.multiply(b);
        return a1;
    }

    // Reverse functions

    // Using `x` in-place of `a` is not reliable, because it may still be incorrect if
    // `a` is greater than `b`. However, I don't see a solution to this
    static int revSLength(NaturalNumber a, NaturalNumber b) {
        NaturalNumber three = new NaturalNumber2(3);
        NaturalNumber grow = new NaturalNumber2(1);
        int result = 0;

        while (true) {
            boolean greaterThanA = grow.compareTo(a) > 0;
            boolean greaterThanB = grow.compareTo(b) > 0;
            if (greaterThanA && greaterThanB) {
                break;
            }

            grow.multiply(three);
            result++;
        }

        return result;
    }

    static Stack2<NaturalNumber> revBs(NaturalNumber b) {
        NaturalNumber three = new NaturalNumber2(3);

        // Clone b
        NaturalNumber b1 = b.newInstance();
        b1.copyFrom(b);

        Stack2<NaturalNumber> result = new Stack2<NaturalNumber>();

        while (!b1.isZero()) {
            // Clone b1
            NaturalNumber item = b.newInstance();
            item.copyFrom(b1);

            result.push(item);

            b1.divide(three);
        }

        return result;
    }

    static Stack2<NaturalNumber> revStack(NaturalNumber x) {
        NaturalNumber three = new NaturalNumber2(3);

        // Clone x
        NaturalNumber x1 = x.newInstance();
        x1.copyFrom(x);

        Stack2<NaturalNumber> result = new Stack2<NaturalNumber>();

        while (!x1.isZero()) {
            // Get remainder
            NaturalNumber r = remainderN(x1, three);

            result.push(r);
            x1.subtract(r);
            x1.divide(three);
        }

        return result;
    }

    static void pad(Stack2<NaturalNumber> s, int desired_length) {
        while (s.length() < desired_length) {
            s.push(new NaturalNumber2(0));
        }
    }

    static Set1L<NaturalNumber> revLoop(
        NaturalNumber a_rem2,
        NaturalNumber b,
        NaturalNumber a_div // a_next
    ) {
        NaturalNumber three = new NaturalNumber2(3);
        NaturalNumber two = new NaturalNumber2(2);
        NaturalNumber one = new NaturalNumber2(1);

        NaturalNumber b_div = divideN(b, three);
        NaturalNumber b_rem1 = remainderN(b, three);
        NaturalNumber b_rem2 = remainderN(b_rem1, two);

        // Set1L<NaturalNumber> a_rem1_adds = new Set1L<NaturalNumber>();
        Set1L<Integer> a_rem1s = new Set1L<Integer>();

        if (a_rem2.equals(two)) {
            if (b_rem2.isZero()) {
                // a_rem1_adds.add(new NaturalNumber2(2));
                a_rem1s.add(0);
            } else {
                // a_rem1_adds.add(new NaturalNumber2(2));
                a_rem1s.add(1);
            }
        } else if (a_rem2.equals(one)) {
            if (b_rem2.isZero()) {
                // a_rem1_adds.add(new NaturalNumber2(4));
                a_rem1s.add(2);
            } else {
                // a_rem1_adds.add(new NaturalNumber2(1));
                a_rem1s.add(0);
            }
        } else if (a_rem2.isZero()) {
            if (b_rem2.isZero()) {
                // a_rem1_adds.add(new NaturalNumber2(3));
                a_rem1s.add(1);
            } else {
                // a_rem1_adds.add(new NaturalNumber2(3));
                a_rem1s.add(2);
            }
        }

        Set1L<NaturalNumber> result = new Set1L<NaturalNumber>();
        for (int a_rem1 : a_rem1s) {
            // a = (3 * a_div) + a_rem1
            NaturalNumber a = new NaturalNumber2();
            a.copyFrom(a_div);
            a.multiply(three);
            a.add(new NaturalNumber2(a_rem1));

            result.add(a);
        }

        return result;
    }

    static Set1L<NaturalNumber> revLoop(Stack2<NaturalNumber> s,
            Stack2<NaturalNumber> bs) {
        Set1L<NaturalNumber> result = new Set1L<NaturalNumber>();
        Set1L<NaturalNumber> prev_result = new Set1L<NaturalNumber>();

        assert bs.length() == s.length();

        while (s.length() > 0) {
            if (result.size() > 100) {
                return result;
            }

            prev_result.transferFrom(result);

            NaturalNumber a_rem2 = s.pop();
            NaturalNumber b = bs.pop();
            if (prev_result.size() > 0) {
                while (prev_result.size() > 0) {
                    NaturalNumber a_div = prev_result.removeAny();
                    Set1L<NaturalNumber> branch_result = revLoop(a_rem2, b,
                            a_div);
                    result.add(branch_result);
                }
            } else {
                NaturalNumber a_div = new NaturalNumber2(0);
                Set1L<NaturalNumber> branch_result = revLoop(a_rem2, b, a_div);
                result.add(branch_result);
            }

            System.out.println("level: " + s.length());
            System.out.println("result: " + result);
        }

        return result;
    }

    static Set1L<NaturalNumber> rev(NaturalNumber x, NaturalNumber b) {
        Stack2<NaturalNumber> s = revStack(x);
        Stack2<NaturalNumber> bs = revBs(b);

        int s_length = revSLength(x, b);
        System.out.println("s_length: " + s_length);
        pad(s, s_length);
        pad(bs, s_length);

        return revLoop(s, bs);
    }
}
