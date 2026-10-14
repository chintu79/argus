# Viva Question Bank

## Basic

1. What is an AI agent?
2. Why is agent evaluation different from conventional software testing?
3. What problem does this project solve?
4. What is an evaluation budget?
5. What is a trajectory?

## Architecture

6. Why is the environment controlled?
7. Why are trajectories logged?
8. Why are state snapshots required?
9. What exactly is being snapshotted?
10. Why are branches useful?

## Security

11. What security failures are evaluated?
12. How are authorization failures detected?
13. How is prompt injection represented?
14. How are tool-level attacks evaluated?
15. How is state leakage detected?

## Adaptive Evaluation

16. Why not test scenarios randomly?
17. What does adaptive selection optimize?
18. Why is cost included?
19. What is exploration versus exploitation?
20. How is selector leakage prevented?

## Failure Analysis

21. What is the difference between a failure candidate and a validated failure?
22. What is a failure family?
23. Why not simply cluster using embeddings?
24. Why is causal root cause not claimed?

## Reproducibility

25. Why must failures be independently reproduced?
26. Why are multiple seeds used?
27. What does Rep_k measure?
28. What makes a reproduction inconclusive?

## Metamorphic Testing

29. What is metamorphic testing?
30. Why is textual output equality insufficient?
31. What constitutes a valid transformation?

## Holdout

32. Why is hidden holdout necessary?
33. How is leakage prevented?
34. What does TSR measure?

## Statistics

35. What is the experimental unit?
36. Why are run-level metrics used?
37. Why use confidence intervals?
38. Why use effect sizes?
39. Why use multiple-comparison correction?
40. What does an inconclusive hypothesis mean?

## Branching

41. How is branching cost measured?
42. Why include snapshot cost?
43. What is prefix-token savings?
44. When could branching become more expensive?

## Limitations

45. What are the largest limitations?
46. Why might results not generalize?
47. How realistic is the simulated environment?
48. What evaluator errors are possible?
49. What happens if the adaptive strategy performs worse?

## Research

50. What is the actual research gap?
51. What is novel?
52. How is novelty distinguished from engineering?
53. What is the strongest evidence supporting the work?
54. What evidence would falsify the central hypothesis?
55. What would you change with more compute?