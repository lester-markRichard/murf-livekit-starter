import { Button } from '@/components/ui/button';

function WelcomeImage() {
  return (
    <div className="mb-4 size-20 rounded-full bg-amber-100 flex items-center justify-center">
      <span className="text-5xl">👋</span>
    </div>
  );
}

interface WelcomeViewProps {
  startButtonText: string;
  onStartCall: () => void;
}

export const WelcomeView = ({
  startButtonText,
  onStartCall,
  ref,
}: React.ComponentProps<'div'> & WelcomeViewProps) => {
  return (
    <div ref={ref}>
      <section className="bg-gradient-to-b from-amber-50 to-orange-50 flex flex-col items-center justify-center min-h-svh text-center px-6">
        <WelcomeImage />

        <h1 className="text-4xl font-bold text-orange-900 mb-2">
          नमस्ते!
        </h1>

        <p className="text-xl text-orange-800 mb-2 font-semibold">
          Hello! I'm your Hindi tutor
        </p>

        <p className="text-base text-orange-700 max-w-prose mb-8 leading-relaxed">
          चलिए मजेदार तरीके से हिंदी सीखते हैं!
          <br />
          Let's learn Hindi together in a fun way!
        </p>

        <Button
          size="lg"
          onClick={onStartCall}
          className="mt-4 px-8 py-6 rounded-full font-bold text-lg bg-amber-500 hover:bg-amber-600 text-white shadow-lg"
        >
          {startButtonText}
        </Button>

        <p className="text-sm text-orange-600 mt-8 max-w-prose">
          Click the button above to start talking. Make sure your microphone is on! 🎤
        </p>
      </section>
    </div>
  );
};
