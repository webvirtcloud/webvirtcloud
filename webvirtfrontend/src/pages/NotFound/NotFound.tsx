import { Link } from 'react-router-dom';
import tw from 'twin.macro';

const Home = (): JSX.Element => {
  return (
    <div css={tw`min-h-screen flex items-center justify-center`}>
      <div css={tw`text-center`}>
        <h1 css={tw`font-bold text-2xl space-y-4`}>Page is not found</h1>
        <Link to="/">Go Home</Link>
      </div>
    </div>
  );
};

export default Home;
