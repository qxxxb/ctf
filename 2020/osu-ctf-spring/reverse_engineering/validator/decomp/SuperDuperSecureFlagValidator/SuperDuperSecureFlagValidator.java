import java.util.StringTokenizer;

public class SuperDuperSecureFlagValidator {
   private static boolean checkFlag(String candidate) {
      try {
         if (!candidate.substring(0, 7).equals("osuctf{")) {
            return false;
         } else if (candidate.charAt(candidate.length() - 1) != '}') {
            return false;
         } else {
            StringTokenizer st = new StringTokenizer(candidate.substring(7, candidate.length() - 1), "_");
            if (!Validator1.verify(st.nextToken())) {
               return false;
            } else if (!Validator2.verify(st.nextToken())) {
               return false;
            } else {
               return !st.hasMoreTokens();
            }
         }
      } catch (Exception var2) {
         return false;
      }
   }

   public static void main(String[] args) throws Exception {
      if (args.length != 1) {
         System.out.println("usage: java -jar SuperSuperSecureFlagValidator.jar <flag>");
      } else {
         String input = args[0];
         if (checkFlag(input)) {
            System.out.println("You got it! The flag is: " + input);
         } else {
            System.out.println("Oops, try again!");
         }

      }
   }
}
