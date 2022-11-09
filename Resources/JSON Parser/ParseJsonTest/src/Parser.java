import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;

public class Parser{
    public static void main(String args[]) throws IOException  //static method
    {
        String file = "src/SVM_JSON";
        String json = new String(Files.readAllBytes(Paths.get(file)));

        ArrayList<String> parsedJson = new ArrayList<String>();
        String currentString = "";
        int parsePointer = 0;
        int bracketCount = 0;
        char currentCharacter;
        for(parsePointer = 0; parsePointer < json.length(); parsePointer++)
        {

            currentCharacter = json.charAt(parsePointer);
            if(currentCharacter == '[')
            {
                bracketCount += 1;
            }
            else if (currentCharacter == ']')
            {
                bracketCount -= 1;
            }

            if(currentCharacter == ',')
            {
                if(bracketCount == 0)
                {
                    parsedJson.add(currentString);
                    currentString = "";
                }
                else
                {
                    currentString = currentString + currentCharacter;
                }
            }
            else
            {
                currentString = currentString + currentCharacter;
            }
        }

        for(int i = 0; i < parsedJson.size(); i++)
        {
            System.out.println(parsedJson.get(i));
        }
    }
}
