import argparse
import sys
from src.tasks import TaskProcessor

def main():
    parser = argparse.ArgumentParser(description="PM Discovery Accelerator CLI")
    parser.add_argument("--research-type", type=str, required=True, 
                        help="Specific research category (e.g. competitor_research, customer_interviews)")
    parser.add_argument("--task", type=str, required=True,
                        help="Specific task within that category (e.g. extract_problems, extract_pain_points)")
    parser.add_argument("--model", type=str, default=None,
                        help="Override default model for this run")
    
    # Placeholder for future expansion like --mutate or --benchmark-subset
    # parser.add_argument("--mutate", action="store_true", help="Enable prompt mutation loop")

    args = parser.parse_args()

    print(f"--- PM Discovery Accelerator ---")
    print(f"Target: {args.research_type} / {args.task}")
    
    try:
        processor = TaskProcessor(args.research_type, args.task, model_override=args.model)
        processor.run()
    except Exception as e:
        print(f"Error during execution: {e}")
        sys.exit(1)

    print(f"--- Done ---")

if __name__ == "__main__":
    main()
