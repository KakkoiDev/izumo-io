# What is good code?

Good code has 3 attributes:
- It works
- It is performant
- It is easy to change

## It works

The code does what you want it to do. Great!

Does it work every time? When you give it the same input, does it produce the expected output every time?

How about when you feed your system the wrong input? Does it handle it? Does it break?

If you want it to break under certain conditions, does it break in the expected way?

And if it breaks, do you know why? Do you know where the error comes from?

## It is performant

Is your system fast enough? Does it fell snappy?

What if we scale it up? More operations, longer processes, will it still be fast?

Sure your hardware has to be be up to the task, but is your code using its resources efficiently?

For example, do you have any `On2` operations in your code? `On2` is big O notation for a loop within a loop.

## Is it easy to change

Ease of change, aka maintainability, requires 2 things:
- Easy to ready code
- Well tested code

Easy to read means that anyone reading your code will have a pretty good idea of how it works.
So it should be written as simply as possible, with a few comments to explain what you intend it to do.
Also, organizing your files well can help.

Well tested code means that you have a way to check that your code does what it is supposed to do.
We often do this with automated tests. Automated tests are functions that check that our code does what it is supposed to do, automatically.
That way, we can have a high degree of confidence that our code does what we want it to do right now.
That it will handle wrong input and edge cases if they ever occur.
And having tests in place guarantees that we can update features without breaking anything in the process.
In complex systems, you don't always know how all the parts are working together.

It often happen that badly tested code bases suffer from "regressions", something that used to work is now broken.
