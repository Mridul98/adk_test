import "@copilotkit/react-ui/styles.css";
import { CopilotChat } from "@copilotkit/react-ui";

export default function YourApp() {
return (
    <main>
    <CopilotChat 
      labels={{
        title: "SQL Documentor Assistant",
        initial: "Hello! I can help you document your SQL code. Just share your SQL snippets or questions, and I'll assist you in creating clear and concise documentation.",
      }}
    />
    </main>
);
}