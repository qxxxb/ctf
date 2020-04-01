import components.naturalnumber.NaturalNumber;
import components.naturalnumber.NaturalNumber2;
import components.stack.Stack2;

public class Validator1 {
   static boolean verify(String s) {
      if (s.charAt(0) == '0') {
         return false;
      } else {
         NaturalNumber b = new NaturalNumber2(s);
         return secretOp(b, new NaturalNumber2("7109340815511137277436103227634468226488145274050")).equals(new NaturalNumber2("135082787268816958421202995954498890820092905902643"));
      }
   }

   static NaturalNumber secretOp(NaturalNumber a, NaturalNumber b) {
      NaturalNumber two = (NaturalNumber)a.newInstance();
      NaturalNumber three = (NaturalNumber)a.newInstance();
      three.setFromInt(2);
      two.setFromInt(3);
      Stack2 s = new Stack2();

      NaturalNumber z1;
      while(!a.isZero() || !b.isZero()) {
         z1 = a.divide(two);
         NaturalNumber z2 = b.divide(two).divide(three);
         if (z2.isZero()) {
            z1.add(three);
         } else {
            z1.increment();
         }

         z1 = z1.divide(two);
         s.push(z1);
      }

      z1 = (NaturalNumber)a.newInstance();

      while(s.length() > 0) {
         z1.multiply(two);
         z1.add((NaturalNumber)s.pop());
      }

      return z1;
   }
}
