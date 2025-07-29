import React from 'react';

interface TestHookComponentProps {
  message: string;
  count: number;
}

const TestHookComponent: React.FC<TestHookComponentProps> = ({ message, count }) => {
  return (
    <div className="test-hook-component">
      <h2>Test Hook Component</h2>
      <p>Message: {message}</p>
      <p>Count: {count}</p>
    </div>
  );
};

export default TestHookComponent;