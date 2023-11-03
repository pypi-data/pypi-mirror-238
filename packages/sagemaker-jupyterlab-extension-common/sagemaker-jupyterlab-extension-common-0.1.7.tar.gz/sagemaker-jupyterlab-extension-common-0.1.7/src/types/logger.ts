import { Token } from '@lumino/coreutils';
import { pluginIds } from '../constants';

interface LogArgumentsContext {
  AccountId: string;
  SpaceName: string;
  SessionId: string;
}

interface ChildLogContext {
  ExtensionName?: string;
  ExtensionVersion?: string;
  ComponentName?: string;
  PluginId?: string;
  WidgetName?: string;
}

interface LogArguments {
  Message?: string;
  Name?: string;
  Stack?: string;
  Error?: Error;
  Context?: LogArgumentsContext & ChildLogContext;
}

type LogMethod = (logArguments: LogArguments) => Promise<void>;

interface ILogger {
  fatal: LogMethod;
  error: LogMethod;
  warn: LogMethod;
  info: LogMethod;
  debug: LogMethod;
  trace: LogMethod;
  child(context: ChildLogContext): ILogger;

  /** SageMaker Studio UI extension version. */
  extensionVersion?: string;
}

enum LogLevel {
  /**
   * Most detailed information. Should only be recorded to console.
   */
  TRACE = 'TRACE',

  /**
   * Detailed information. Should only be recorded to console.
   */
  DEBUG = 'DEBUG',

  /**
   * Expected and desirable runtime events. Requests, responses, application startup, etc.
   */
  INFO = 'INFO',

  /**
   * Undesirable runtime events that should not crash the application.
   */
  WARN = 'WARN',

  /**
   * Runtime errors that might cause an application crash.
   */
  ERROR = 'ERROR',

  /**
   * Runtime errors that are expected to cause an application crash.
   */
  FATAL = 'FATAL',
}

const ILogger = new Token<ILogger>(pluginIds.LoggerPlugin);

export { ILogger, LogArgumentsContext, ChildLogContext, LogArguments, LogLevel };
